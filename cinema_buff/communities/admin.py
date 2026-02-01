from django.contrib import admin
from .models import Community, CommunityMember

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'member_count', 'created_at']
    list_filter = ['genre', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['member_count', 'created_at', 'updated_at']

@admin.register(CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'is_admin', 'joined_at']
    list_filter = ['is_admin', 'joined_at', 'community']
    search_fields = ['user__username', 'community__name']
    readonly_fields = ['joined_at']
