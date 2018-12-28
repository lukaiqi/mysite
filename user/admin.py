from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Phone_Profile, Avatar


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class Phone_ProfileInline(admin.StackedInline):
    model = Phone_Profile
    can_delete = False


class AvatarInline(admin.StackedInline):
    model = Avatar
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, Phone_ProfileInline,)
    list_display = ('username', 'nickname', 'phone', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname

    def phone(self, obj):
        return obj.phone_profile.phone

    def avatar(self, obj):
        return obj.user_avatar.avatar

    nickname.short_description = '昵称'
    phone.short_description = '电话'
    avatar.short_description = '头像'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')


@admin.register(Phone_Profile)
class Phone_ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
