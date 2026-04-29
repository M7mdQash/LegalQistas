from django.contrib import admin
from .models import UserProfile, LawyerProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_lawyer']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']

    @admin.display(boolean=True, description='Lawyer')
    def is_lawyer(self, obj):
        return obj.is_lawyer


@admin.register(LawyerProfile)
class LawyerProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    autocomplete_fields = ['user']
