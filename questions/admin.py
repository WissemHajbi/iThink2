from django.contrib import admin
from .models import questions, answered

admin.site.register(questions)
admin.site.register(answered)