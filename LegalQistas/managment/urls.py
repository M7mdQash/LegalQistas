from django.urls import path
from . import views

app_name = 'managment'

# Full pages (render views)
urlpatterns = [
    path('',                           views.dashboard,              name='dashboard'),
    path('users/',                     views.user_list,              name='user_list'),
    path('sessions/',                  views.session_list,           name='session_list'),
    path('sessions/<int:pk>/',         views.session_detail,         name='session_detail'),
    path('contacts/',                  views.contact_requests,       name='contact_requests'),

    # Action-only URLs (POST → redirect, no render)
    path('users/<int:pk>/assign/',     views.assign_lawyer,          name='assign_lawyer'),
    path('users/<int:pk>/revoke/',     views.revoke_lawyer,          name='revoke_lawyer'),
    path('sessions/<int:pk>/status/',  views.update_session_status,  name='update_session_status'),
    path('sessions/<int:pk>/assign/',  views.reassign_session,       name='reassign_session'),
    path('contacts/<int:pk>/read/',    views.mark_contact_read,      name='mark_contact_read'),
    
    # ========== waiting on integration with posts app
    path('posts/',                     views.post_list,              name='post_list'),
    path('posts/<int:pk>/publish/',    views.toggle_publish,         name='toggle_publish'),
    path('posts/<int:pk>/delete/',     views.delete_post,            name='delete_post'),

]
