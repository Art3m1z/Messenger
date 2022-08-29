from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),

    path('create-form/', views.create_room, name='create-room'),
    path('update-form/<str:pk>/', views.update_form, name='update-form'),
    path('delete-form/<str:pk>/', views.delete_form, name='delete_form'),
    path('delete_message/<str:pk>/', views.delete_message, name='delete_message'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    path('user_update/', views.user_update, name='user_update'),
    path('topics/', views.browse_topic, name='browse_topic'),
    path('activity/', views.browse_activities, name='browse_activity'),

]