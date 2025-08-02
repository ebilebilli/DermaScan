import openai
from celery import shared_task
from django.conf import settings
from users.models import CustomerUser
from scans.models import Diagnosis, SkinImage, ProductRecommendation
from chats.models import ChatMessage


openai.api_key = settings.OPENAI_TOKEN


@shared_task
def ai_response_model_task(message=None, image_id=None, user_id=None):
    prompt = ""
    
    if image_id:
        try:
            image = SkinImage.objects.get(id=image_id)
            user = image.user
        except SkinImage.DoesNotExist:
            return {'error': f'SkinImage with ID {image_id} not found.'}

        prompt = (
            "You are a professional AI dermatologist.\n"
            "A user has uploaded a close-up skin image for diagnosis.\n"
            "Your task is to analyze the image (assume it's provided) and identify the most likely skin condition.\n"
            "Provide:\n"
            "1. A short, clear medical label (the condition name),\n"
            "2. A concise, user-friendly description of the condition,\n"
            "3. An estimated confidence score (between 0 and 1).\n\n"
            "Respond in this format:\n"
            "Label: <condition_name>\n"
            "Description: <short_explanation>\n"
            "Confidence: <confidence_score>"
        )
    elif message:
        user = CustomerUser.objects.get(id=user_id)
        prompt = (
            f"A user has asked the following skin-related question:\n\n"
            f"Message: {message}\n\n"
            "You are an AI dermatologist assistant. Please answer the question in a helpful, clear, and concise way."
        )
    else:
        return {'error': 'Neither image nor message provided.'}

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {'role': 'system', 'content': 'You are an AI skin diagnostic tool. Respond medically and clearly.'},
            {'role': 'user', 'content': prompt},
        ],
        max_tokens=500,
        temperature=0.6
    )

    content = response.choices[0].message.content.strip()

    if image_id:
        lines = content.splitlines()
        label = lines[0].replace("Label:", "").strip()
        description = lines[1].replace("Description:", "").strip()
        confidence_str = lines[2].replace("Confidence:", "").strip()

        try:
            confidence = float(confidence_str)
        except ValueError:
            confidence = None

        Diagnosis.objects.create(
            user=user,
            image=image,
            label=label,
            description=description,
            confidence=confidence,
            ai_response=content
        )
        ChatMessage.objects.create(
            sender=ChatMessage.AI,
            user=user,
            message=content
        )
        return content

    else:
        ChatMessage.objects.create(
            sender=ChatMessage.AI,
            user=user,
            message=content
        )
        return content
