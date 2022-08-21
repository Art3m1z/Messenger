from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-form/', views.create_room, name='create-room'),
    path('update-form/<str:pk>/', views.update_form, name='update-form'),
    path('delete-form/<str:pk>/', views.delete_form, name='delete-form'),
]