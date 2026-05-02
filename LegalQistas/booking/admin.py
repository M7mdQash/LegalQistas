from django.contrib import admin
from .models import TimeSlot, BookingSession, Message, ContactRequest


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['lawyer', 'date', 'start_time', 'end_time', 'is_available']
    list_filter = ['is_available', 'date']
    list_editable = ['is_available']
    search_fields = ['lawyer__username', 'lawyer__first_name', 'lawyer__last_name']


@admin.register(BookingSession)
class BookingSessionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'customer', 'lawyer', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['customer__username', 'lawyer__username']
    autocomplete_fields = ['customer', 'lawyer']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'sent_at']
    search_fields = ['sender__username', 'body']


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'is_read']
    list_filter = ['is_read']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'subject']
