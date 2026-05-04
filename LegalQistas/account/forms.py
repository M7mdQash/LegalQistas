from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import LawyerProfile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'profile_image']


class LawyerProfileForm(forms.ModelForm):
    class Meta:
        model = LawyerProfile
        fields = ['avatar', 'about_me', 'certificates', 'resume']
        widgets = {
            'about_me': forms.Textarea(attrs={'rows': 5}),
        }
