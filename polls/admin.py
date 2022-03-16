from django.contrib import admin
from .models import poll, user, voted, deleted


admin.site.register(poll)
admin.site.register(user)
admin.site.register(voted)
admin.site.register(deleted)