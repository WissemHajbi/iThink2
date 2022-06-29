from django.contrib import admin
from .models import poll, user, voted, deleted, poll_comment


admin.site.register(poll)
admin.site.register(user)
admin.site.register(voted)
admin.site.register(deleted)
admin.site.register(poll_comment)