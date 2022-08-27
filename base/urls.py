from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),

    path('create-form/', views.create_room, name='create-room'),
    path('update-form/<str:pk>/', views.update_form, name='update-form'),
    path('delete-form/<str:pk>/', views.delete_form, name='delete-form'),
    path('delete_message/<str:pk>/', views.delete_message, name='delete_message'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

]