
from django.db import models
from polls.models import user
from django.urls import reverse


class questions(models.Model):

    status = (
        ("approved", "approved"),
        ("disapproved", "disapproved")
    )

    status = models.CharField(
        max_length=11, choices=status, default="disapproved")

    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question[:150]+"..." if len(self.question) > 150 else self.question

    def get_absolute_url(self):
        return reverse("home")


class answered(models.Model):

    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='answered_questions')
    question = models.ForeignKey(questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
