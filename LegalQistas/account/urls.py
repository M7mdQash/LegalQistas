from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('signup/success/', views.sign_up_success, name='sign_up_success'),
    path('signin/', views.sign_in, name='sign_in'),
    path('signout/', views.sign_out, name='sign_out'),
    path('profile/<int:pk>/', views.profile_view, name='profile_view'),
    path('profile/<int:pk>/edit/', views.profile_edit_view, name='profile_edit'),
]
