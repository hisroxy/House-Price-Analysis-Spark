from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.dashboard_data, name='dashboard_data'),
    path('summary/', views.dashboard_summary, name='dashboard_summary'),
]