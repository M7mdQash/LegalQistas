from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.get_full_name() or self.user.username}'

    @property
    def is_lawyer(self):
        return self.user.groups.filter(name='lawyer').exists()


class LawyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lawyer_profile')
    avatar = models.ImageField(upload_to='lawyer_avatars/', blank=True, null=True)
    about_me = models.TextField(blank=True)
    certificates = models.ImageField(upload_to='lawyer_certificates/', blank=True, null=True)
    resume = models.FileField(upload_to='lawyer_resumes/', blank=True, null=True)

    def __str__(self):
        return f'Lawyer profile of {self.user.get_full_name() or self.user.username}'
