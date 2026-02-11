from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('user-info/', views.get_user_info, name='get_user_info'),
    path('update-info/', views.update_user_info, name='update_user_info'),
    path('favorites/', views.get_user_favorites, name='get_user_favorites'),
    path('comments/', views.get_user_comments, name='get_user_comments'),
    path('browse-history/', views.get_user_browse_history, name='get_user_browse_history'),
    path('click-behaviors/', views.get_user_click_behaviors, name='get_user_click_behaviors'),
]