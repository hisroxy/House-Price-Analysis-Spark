from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('user-info/', views.get_user_info, name='get_user_info'),
]