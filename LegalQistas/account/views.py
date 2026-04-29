from django.shortcuts import render, redirect
from .forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sign_up_success')
    else:
        form = SignUpForm()
    return render(request, 'account/sign_up.html', {'form': form})


def sign_up_success(request):
    return render(request, 'account/sign_up_success.html')
