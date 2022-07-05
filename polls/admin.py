from django.contrib import admin
from .models import poll, user, voted, deleted, poll_comment


# to show the id column
class idAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(poll_comment, idAdmin)
admin.site.register(poll, idAdmin)
admin.site.register(user, idAdmin)
admin.site.register(voted, idAdmin)
admin.site.register(deleted, idAdmin)
