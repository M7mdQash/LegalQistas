from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import SignUpForm, LawyerProfileForm
from .models import UserProfile, LawyerProfile, GROUP_CLIENT
from django.http import HttpRequest


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
                client_group, _ = Group.objects.get_or_create(name=GROUP_CLIENT)
                user.groups.add(client_group)
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

def sign_out(request):
    logout(request)
    return redirect('/')

# _____________________ Profile section of views _____________________

def profile_view(request: HttpRequest, pk: int):
    profile_user = get_object_or_404(User, pk=pk)
    lawyer_profile = get_object_or_404(LawyerProfile, user=profile_user)
    user_profile = get_object_or_404(UserProfile, user=profile_user)
    return render(request, 'account/profile.html', {
        'profile_user': profile_user,
        'lawyer_profile': lawyer_profile,
        'user_profile': user_profile,
    })


@login_required
def profile_edit_view(request: HttpRequest, pk: int):
    profile_user = get_object_or_404(User, pk=pk)
    lawyer_profile = get_object_or_404(LawyerProfile, user=profile_user)

    if request.user.pk != pk:
        return redirect('account:profile_view', pk=pk)

    if request.method == 'POST':
        form = LawyerProfileForm(request.POST, request.FILES, instance=lawyer_profile)
        if form.is_valid():
            form.save()
            return redirect('account:profile_view', pk=pk)
    else:
        form = LawyerProfileForm(instance=lawyer_profile)

    return render(request, 'account/profile_edit.html', {
        'form': form,
        'profile_user': profile_user,
    })
    
