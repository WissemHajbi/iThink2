from django.urls import path
from .views import question_suggestion ,answer, delete_comment_question
from polls.views import profileView

urlpatterns = [
    path("question_suggestion", question_suggestion.as_view(), name="question_suggestion"),
    path('question/<int:pk>', answer, name="question_answer"),
    path('profile/<str:name>', profileView.as_view(), name="profile"),
    path("delete_comment_question/<int:id>/<int:pk>", delete_comment_question, name="delete_comment_question")
]