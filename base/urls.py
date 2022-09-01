from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('room/<str:pk>/', views.RoomPage.as_view(), name='room'),
    path('profile/<str:pk>/', views.UserProfile.as_view(), name='user_profile'),

    path('create-form/', views.CreateRoom.as_view(), name='create-room'),
    path('update-form/<str:pk>/', views.UpdateForm.as_view(), name='update-form'),
    path('delete-form/<str:pk>/', views.DeleteRoom.as_view(), name='delete_form'),
    path('delete_message/<str:pk>/', views.DeleteMessage.as_view(), name='delete_message'),

    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),

    path('user_update/', views.UserUpdate.as_view(), name='user_update'),
    path('topics/', views.BrowseTopic.as_view(), name='browse_topic'),
    path('activity/', views.BrowseActivities.as_view(), name='browse_activity'),

]