from django.contrib import admin
from .models import question, question_answered, question_comment

admin.site.register(question)
admin.site.register(question_answered)
admin.site.register(question_comment)