from django.urls import path
from .views import question_suggestion ,answer
from polls.views import profileView

urlpatterns = [
    path("question_suggestion", question_suggestion.as_view(), name="question_suggestion"),
    path('question/<int:pk>', answer, name="question_answer"),
    path('profile/<str:name>', profileView.as_view(), name="profile"),
]