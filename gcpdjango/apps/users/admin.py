from django.contrib import admin
from gcpdjango.apps.users.models import User, Group


class GroupAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "owners",
    )


admin.site.register(User)
admin.site.register(Group, GroupAdmin)
