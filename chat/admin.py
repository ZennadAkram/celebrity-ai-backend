from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Celebrity, ChatSession, Message

# Extend the default UserAdmin to include your custom fields
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_avatar',)}),  # add your extra field
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_avatar',)}),
    )

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Celebrity)
admin.site.register(ChatSession)
admin.site.register(Message)
from .models import Category
admin.site.register(Category)
