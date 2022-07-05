from django.contrib import admin
from .models import question, question_answered, question_comment

class idadmin(admin.ModelAdmin):
    readonly_fields = ("id",)

admin.site.register(question, idadmin)
admin.site.register(question_answered, idadmin)
admin.site.register(question_comment, idadmin)