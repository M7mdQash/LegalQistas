from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
# Create your views here.

def home_view(request:HttpRequest):

    return render(request, 'main/home.html')


def services_view(request:HttpRequest):

    return render(request, 'main/services.html')

def lawyers_view(request:HttpRequest):

    return render(request, 'main/lawyers.html')

def about_view(request:HttpRequest):

    return render(request, 'main/about.html')

def contact_view(request:HttpRequest):

    return render(request, 'main/contact.html')

def mode_view(request, mode):

    next_url = request.GET.get("next", "/")

    if mode == "toggle":
        current_mode = request.COOKIES.get("mode", "light")
        mode = "dark" if current_mode == "light" else "light"

    response = redirect(next_url)
    response.set_cookie("mode", mode)

    return 
    
    