from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_view, name='posts_view'),
    path('create/', views.create_post_view, name='create_post_view'),
    path('<slug:slug>/', views.post_detail_view, name='post_detail_view'),
    path('<slug:slug>/update/', views.update_post_view, name='update_post_view'),
    path('<slug:slug>/delete/', views.delete_post_view, name='delete_post_view')
       
]