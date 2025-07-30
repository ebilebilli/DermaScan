import openai
from celery import shared_task
from django.conf import settings

from movies.models.movie import Movie


openai.api_key = settings.OPENAI_TOKEN

@shared_task()
def generate_ai_response_task(question, message):

    movie_count = Movie.objects.filter(is_active=True).count()
    prompt = f"""
    Question of user: {question}
    \nAnswer find in database: {message}
    \nGive simple and clear answer
    \nOur site currently has {movie_count} active movie
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': 'You are movie website.'},
                {'role': 'user', 'content': prompt},
            ],
            max_tokens=200,  
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content']
        return {'answer': answer}
    
    except Exception as e:
         return f'AI error: {str(e)}'