from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class poll(models.Model):

    genres = (
        ('p', 'politics'),
        ('s', 'sports'),
        ('g', 'gaming'),
        ('h', 'health'),
        ('m', 'music'),
    )

    question = models.CharField(max_length=80)

    genre = models.CharField(max_length=10, choices=genres, default="")

    answer1 = models.CharField(max_length=200, blank=True, null=True)
    count1 = models.IntegerField(default=0)

    answer2 = models.CharField(max_length=200, blank=True, null=True)
    count2 = models.IntegerField(default=0)

    answer3 = models.CharField(max_length=200, blank=True, null=True)
    count3 = models.IntegerField(default=0)

    answer4 = models.CharField(max_length=200, blank=True, null=True)
    count4 = models.IntegerField(default=0)

    answer5 = models.CharField(max_length=200, blank=True, null=True)
    count5 = models.IntegerField(default=0)

    answer6 = models.CharField(max_length=200, blank=True, null=True)
    count6 = models.IntegerField(default=0)


class user(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    username = models.CharField(max_length=100)
    started_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=255, unique=True)
    
    USERNAME_FIELD = "email"
    
    
    def __str__(self):
        return self.username


class voted(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    poll = models.ForeignKey(poll, on_delete=models.CASCADE)
    choice = models.IntegerField(default=0)
    def __str__(self):
        return f"{user} voted in {poll.id}"


class deleted(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    poll = models.ForeignKey(poll, on_delete=models.CASCADE)

    def __str__(self):
        return f"{user} deleted {poll.id}"
