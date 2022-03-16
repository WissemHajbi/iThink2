from django.db import models
from polls.models import user


class questions(models.Model):

    question = models.CharField(max_length=200)


class answered(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    question = models.ForeignKey(questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
