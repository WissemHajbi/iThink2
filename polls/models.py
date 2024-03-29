from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json, random


class user(models.Model):

    genders = (
        ('m', 'male'),
        ('f', 'female'),
    )

    profile_picture_numbers = (
        ("['1']", '1'),
        ("['2']", '2'),
        ("['3']", '3'),
        ("['4']", '4'),
        ("['5']", '5'),
        ("['6']", '6'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    username = models.CharField(max_length=30)
    gender = models.CharField(max_length=6, choices=genders)
    started_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=255, unique=True)
    profile_picture_number = models.CharField(
        max_length=10, choices=profile_picture_numbers)
    cover_picture_number = models.IntegerField(default=3)

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username


class poll(models.Model):

    genres = (
        ('p', 'politics'),
        ('s', 'sports'),
        ('g', 'gaming'),
        ('h', 'health'),
        ('m', 'music'),
    )

    status = (
        ('approved', 'approved'),
        ('pending', 'pending'),
        ('disapproved', 'disapproved')
    )

    creator = models.CharField(max_length=30)

    status = models.CharField(
        max_length=11, choices=status, default="pending")

    question = models.CharField(max_length=200)

    genre = models.CharField(max_length=10, choices=genres)

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

    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question[:100]+"..." if len(self.question) > 100 else self.question

    def make():

        with open("Ithink2/databaseSheet.json", "r") as sheet:
            data = json.load(sheet)
            
        random.shuffle(data["polls"])
        
        for i in range(len(data["polls"])):
            print(i)
            myPoll = poll(
                genre=data["polls"][i]["genre"],
                creator=data["polls"][i]["creator"],
                question=data["polls"][i]["question"],
                status="approved",
            )
            if data["polls"][i]["answer1"]:
                myPoll.answer1 = data["polls"][i]["answer1"]
            if data["polls"][i]["answer2"]:
                myPoll.answer2 = data["polls"][i]["answer2"]
            if data["polls"][i]["answer3"]:
                myPoll.answer3 = data["polls"][i]["answer3"]
            if data["polls"][i]["answer4"]:
                myPoll.answer4 = data["polls"][i]["answer4"]
            if data["polls"][i]["answer5"]:
                myPoll.answer5 = data["polls"][i]["answer5"]
            if data["polls"][i]["answer6"]:
                myPoll.answer6 = data["polls"][i]["answer6"]
                
            myPoll.save()
            
    def delete(self):
        for i in range(6):
            if poll.objects.filter(question=self.data["polls"][i]["question"]):
                poll.objects.filter(
                    question=self.data["polls"][i]["question"]).delete()
 

class voted(models.Model):
    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='voted_polls')
    poll = models.ForeignKey(poll, on_delete=models.CASCADE)
    choice = models.IntegerField(default=0)

    def __str__(self):
        poll = self.poll.question[:100] + \
            "..." if len(self.poll.question) > 100 else self.poll.question
        return f"{self.user.username} voted in '' {poll} '' "


class deleted(models.Model):

    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="deleted_polls")
    poll = models.ForeignKey(poll, on_delete=models.CASCADE)

    def __str__(self):
        poll = self.poll.question[:100] + \
            "..." if len(self.poll.question) > 100 else self.poll.question
        return f"{self.user.username} deleted '' {poll} '' "


class poll_comment(models.Model):

    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="comments_polls")
    poll = models.ForeignKey(poll, on_delete=models.CASCADE)
    comment_str = models.CharField(max_length=300, default="empty")
    date = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)

    # id = models.CharField(max_length=50, default="0")
    class Meta:
        managed = True

    def __str__(self):
        poll = self.poll.question[:100] + \
            "..." if len(self.poll.question) > 100 else self.poll.question
        return f"{self.user.username} commented on '' {poll} '' "


