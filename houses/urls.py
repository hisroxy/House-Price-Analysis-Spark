from django.urls import path
from . import views

app_name = 'houses'

urlpatterns = [
    path('list/', views.house_list, name='house_list'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('detail/<str:house_id>/', views.house_detail, name='house_detail'),
    path('comments/<str:house_id>/', views.house_comments, name='house_comments'),
    path('add-comment/<str:house_id>/', views.add_comment, name='add_comment'),
]