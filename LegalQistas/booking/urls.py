from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('book/',                        views.book_session,    name='book_session'),
    path('sessions/',                    views.session_list,    name='session_list'),
    path('sessions/<int:pk>/',           views.session_detail,  name='session_detail'),
    path('sessions/<int:pk>/message/',   views.send_message,    name='send_message'),
    path('schedule/',                    views.lawyer_schedule, name='lawyer_schedule'),
    path('contact/',                     views.contact_form,    name='contact_form'),
    path('contact/success/',             views.contact_success, name='contact_success'),
]
