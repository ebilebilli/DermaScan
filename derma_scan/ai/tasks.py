import openai
from celery import shared_task
from django.conf import settings
from scans.models import Diagnosis, SkinImage, ProductRecommendation
from chats.models import ChatMessage

openai.api_key = settings.OPENAI_TOKEN

@shared_task
def ai_response_model_task(message=None, image_id=None):
    if not image_id and not message:
        return {'error': 'Neither image nor message provided.'}

    user = None
    full_image_url = None
    prompt = ""

    if image_id:
        try:
            image = SkinImage.objects.get(id=image_id)
            user = image.user
            image_url = image.file.url
            full_image_url = f"{settings.SITE_DOMAIN}{image_url}"
        except SkinImage.DoesNotExist:
            return {'error': f'SkinImage with ID {image_id} not found.'}

        prompt = (
            "You are a professional AI dermatologist.\n"
            "A user has uploaded a close-up skin image for diagnosis.\n"
            "Analyze the image and identify the most likely skin condition.\n"
            "Provide:\n"
            "1. A short, clear medical label (condition name)\n"
            "2. A concise, user-friendly description\n"
            "3. Confidence score (0-1)\n\n"
            "4. Recommend a suitable product name for treatment.\n\n"
            "Respond in format:\n"
            "Label: <condition_name>\n"
            "Description: <short_explanation>\n"
            "Confidence: <confidence_score>"
            "Product: <product_name>"
        )

    else:
        user = message.user
        prompt = (
            f"A user has asked the following skin-related question:\n\n"
            f"Message: {message}\n\n"
            "You are an AI dermatologist assistant. Please answer clearly and concisely."
        )

    user_content = [{"type": "text", "text": prompt}]
    if full_image_url:
        user_content.append({"type": "image_url", "image_url": {"url": full_image_url}})

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional AI dermatologist."},
            {"role": "user", "content": user_content}
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
        product_name = lines[3].replace("Product:", "").strip()

        try:
            confidence = float(confidence_str)
        except ValueError:
            confidence = None

        diagnosis = Diagnosis.objects.create(
            user=user,
            image=image,
            label=label,
            description=description,
            confidence=confidence,
            ai_response=content
            )
        
        ProductRecommendation.objects.create(
            user=user,
            diagnosis=diagnosis,
            name=product_name
        )

        image.is_analyzed = True
        image.save()

    ChatMessage.objects.create(
        sender=ChatMessage.AI,
        user=user,
        message=content
    )

    return content
