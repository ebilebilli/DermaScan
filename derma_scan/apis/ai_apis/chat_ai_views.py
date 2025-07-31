from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from movies.models.movie import Movie
from ai.tasks import generate_ai_response_task


__all__ = [
    'AITaskRequestAPIView',
    'AITaskResponseAPIView',
]

class AITaskRequestAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def post(self, request):
        question = request.data.get('question', '')
        if not question:
            return Response({'error': 'There is no any question'})
        
        find_movie = Movie.objects.filter(title__icontains=question, is_active=True).first()
        if find_movie:
            movie_url = request.build_absolute_uri(f'/api/v1/movies/{find_movie.slug}/')
            message = f'{find_movie} is active on our website\nThere is url for movie: {movie_url}'
        
        else:
            message = f'Sorry, there is not such movie on our website'

        task  = generate_ai_response_task.delay(question=question, message=message)
        return Response({'task_id': task.id}, status=status.HTTP_200_OK)


class AITaskResponseAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        if task_result.ready():
            return Response({'result': task_result.get()}, status=200)
         
        return Response({'status': 'processing'}, status=202)
    