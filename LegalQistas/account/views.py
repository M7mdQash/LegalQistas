from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:home_view')
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
