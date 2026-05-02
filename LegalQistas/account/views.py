from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .forms import SignUpForm
from .models import UserProfile


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                profile_image = form.cleaned_data.get('profile_image')
                UserProfile.objects.create(user=user, profile_image=profile_image)
                return redirect('main:home_view')
            except IntegrityError:
                form.add_error('email', 'A user with that email already exists.')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = SignUpForm()
    return render(request, 'account/sign_up.html', {'form': form})


def sign_up_success(request):
    return render(request, 'account/sign_up_success.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, 'account/sign_in.html', {'form': {'errors': True}})
    return render(request, 'account/sign_in.html', {'form': {}})
