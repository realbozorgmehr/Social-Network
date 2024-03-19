from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Relations, Profile


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.register(Relations)
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
