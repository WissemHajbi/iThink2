from django.urls import path
from .views import answer


urlpatterns = [
    path('question/<int:pk>', answer, name="question_answer"),
]