from django.contrib import admin
from .models import UserProfile, UserConnection

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'bio']
    filter_horizontal = ['favorite_genres']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserConnection)
class UserConnectionAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['from_user__username', 'to_user__username']
    readonly_fields = ['created_at']
