from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('signup/success/', views.sign_up_success, name='sign_up_success'),
]
