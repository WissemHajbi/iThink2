
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from django.utils import timezone
import json
from polls.models import user, poll


class question(models.Model):

    status = (
        ("approved", "approved"),
        ("pending", "pending"),
        ("disapproved", "disapproved")
    )

    status = models.CharField(
        max_length=11, choices=status, default="pending")

    question = models.CharField(max_length=200)

    creator = models.CharField(max_length=30)

    created_time = models.DateTimeField(default=timezone.now)

    def make():

        with open("Ithink2/databaseSheet.json", "r") as sheet:
            data = json.load(sheet)

        for i in range(len(data["questions"])):
            myQuestion = question(
                creator=data["questions"][i]["creator"],
                question=data["questions"][i]["question"],
                status="approved"
            )

            myQuestion.save()

    def __str__(self):
        return self.question[:150]+"..." if len(self.question) > 150 else self.question

    def get_absolute_url(self):
        return reverse("home")


class question_answered(models.Model):

    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='answered_question')
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        question = self.question.question[:100] + \
            "..." if len(
                self.question.question) > 100 else self.question.question
        return f"{self.user.username} answered '' {question} '' "


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


class notification(models.Model):

    status = (
        ('cleared', 'cleared'),
        ('not_cleared', 'not_cleared')
    )

    notification_text = models.CharField(max_length=200)
    notification_status = models.CharField(
        max_length=13, choices=status, default="not_cleared")
    notification_date = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(
        user, on_delete=models.CASCADE)
    poll = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} has a notification"

# status changing notifications


@receiver(pre_save, sender=poll)
def change_status(sender, instance,  **kwargs):
    try:
        if sender.objects.get(id=instance.id).status != instance.status:
            if instance.status == "approved":
                notif = notification.objects.create(
                    notification_text="your poll has been approved",
                    poll=instance.id,
                    user=user.objects.get(username=instance.creator)
                )
                notif.save()
            elif instance.status == "disapproved":
                notif = notification.objects.create(
                    notification_text="your poll has been disapproved, you may want to check it",
                    poll=instance.id,
                    user=user.objects.get(username=instance.creator)
                )
            notif.save()
    except Exception as e:
        # if the object is still not created
        print(e)


@receiver(pre_save, sender=question)
def change_status(sender, instance,  **kwargs):
    try:
        if sender.objects.get(id=instance.id).status != instance.status:
            if instance.status == "approved":
                notif = notification.objects.create(
                    notification_text="your question has been approved",
                    question=instance.id,
                    user=user.objects.get(username=instance.creator)
                )
                notif.save()
            elif instance.status == "disapproved":
                notif = notification.objects.create(
                    notification_text="your question has been disapproved, you may want to check it",
                    question=instance.id,
                    user=user.objects.get(username=instance.creator)
                )
            notif.save()
    except Exception as e:
        # if the object is still not created
        pass
