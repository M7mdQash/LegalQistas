from django.db import models
from django.contrib.auth.models import User


class TimeSlot(models.Model):
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('lawyer', 'date', 'start_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.lawyer.get_full_name()} — {self.date} {self.start_time}'


class BookingSession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('rescheduled', 'Rescheduled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Session #{self.pk} — {self.customer.get_full_name()} with {self.lawyer.get_full_name()}'


class Message(models.Model):
    session = models.ForeignKey(BookingSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        #TODO:  make sure that the session passes its real id 
        return f'Message from {self.sender.get_full_name()} in session #{self.session.pk}'



class ContactRequest(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'