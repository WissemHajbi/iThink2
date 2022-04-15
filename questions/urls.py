from django.urls import path
from .views import question_suggestion ,answer


urlpatterns = [
    path('question/<int:pk>', answer, name="question_answer"),
    path("question_suggestion", question_suggestion.as_view(), name="question_suggestion"),
]