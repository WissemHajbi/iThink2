
from django.db import models
from polls.models import user
from django.urls import reverse
from django.utils import timezone
import json


class question(models.Model):

    status = (
        ("approved", "approved"),
        ("disapproved", "disapproved")
    )

    status = models.CharField(
        max_length=11, choices=status, default="disapproved")

    question = models.CharField(max_length=200)

    creator = models.CharField(max_length=30)

    def make():
        with open("Ithink2/databaseSheet.json", "r") as sheet:
            data = json.load(sheet)

        for i in range(2):
            myQuestion = question(
                creator=data["question"][i]["creator"],
                question=data["question"][i]["question"],
                status="approved"
            )

            myQuestion.save()

    def __str__(self):
        return self.question[:150]+"..." if len(self.question) > 150 else self.question

    def get_absolute_url(self):
        return reverse("home")


# lunch this function when you want to make some default question for testing
testing_Poll_instance = question()


class question_answered(models.Model):

    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='answered_question')
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)


class question_comment(models.Model):

    user = models.ForeignKey(
        user, on_delete=models.CASCADE)
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    comment_str = models.CharField(max_length=300, default="empty")
    date = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)

    class Meta:
        managed = True

    def __str__(self):
        question = self.question.question[:100]+"..." if len(
            self.question.question) > 100 else self.question.question
        return f"{self.user.username} commented on '' {question} '' "
