import openai
from celery import shared_task
from django.conf import settings
from scans.models import Diagnosis, SkinImage, ProductRecommendation

openai.api_key = settings.OPENAI_TOKEN


@shared_task
def generate_diagnosis_task(image_id):
    image = SkinImage.objects.get(id=image_id)

    prompt = (
    "You are a professional AI dermatologist.\n"
    "A user has uploaded a close-up skin image for diagnosis.\n"
    "Your task is to analyze the image (assume it's provided) and identify the most likely skin condition.\n"
    "Provide:\n"
    "1. A short, clear medical label (the condition name),\n"
    "2. A concise, user-friendly description of the condition,\n"
    "3. An estimated confidence score (between 0 and 1) representing how confident you are in your diagnosis.\n\n"
    "Respond strictly in the following format:\n"
    "Label: <condition_name>\n"
    "Description: <short_explanation>\n"
    "Confidence: <confidence_score>"
    )


    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {'role': 'system', 'content': 'You are an AI skin diagnostic tool. Keep answers short and medically relevant.'},
            {'role': 'user', 'content': prompt},
        ],
        max_tokens=300,
        temperature=0.5
    )

    content = response.choices[0].message.content.strip()
    lines = content.splitlines()

    label = lines[0].replace("Label:", "").strip()
    description = lines[1].replace("Description:", "").strip()
    confidence_str = lines[2].replace("Confidence:", "").strip()

    try:
        confidence = float(confidence_str)
    except ValueError:
        confidence = None 

    diagnosis = Diagnosis.objects.create(
        user=image.user,
        image=image,
        label=label,
        description=description,
        confidence=confidence
    )
    generate_diagnosis_response_task.delay(diagnosis.id)
    

@shared_task()
def generate_diagnosis_response_task(diagnosis_id):
    try:
        diagnosis = Diagnosis.objects.select_related("image__user").get(id=diagnosis_id)
        user = diagnosis.image.user
        description = diagnosis.description
        label = diagnosis.label
        confidence = diagnosis.confidence

        prompt = (
            "A user has uploaded a skin image and received the following AI-based diagnosis:\n"
            f"- Condition: {label}\n"
            f"- Description: {description}\n\n"
            f"- confidence: {confidence}\n"
            "Please generate a concise, easy-to-understand explanation of the condition suitable for the user. "
            "Also, recommend 2-3 skincare products that may help address the issue, including product name, short reason, and (optional) URL."
        )

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {'role': 'system', 'content': 'You are a focused and professional AI dermatologist assistant. Stay on topic and avoid unnecessary commentary.'},
                {'role': 'user', 'content': prompt},
            ],
            max_tokens=500,
            temperature=0.6
        )

        content = response.choices[0].message.content.strip()
        diagnosis.ai_response = content
        diagnosis.save()

        return  content

    except Diagnosis.DoesNotExist:
        return {'error': f'Diagnosis with ID {diagnosis_id} not found.'}
    except Exception as e:
        return {'error': str(e)}
