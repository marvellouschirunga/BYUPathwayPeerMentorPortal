from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# URL patterns for the application
urlpatterns = [

    # Account Activation URL
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    # Handles user account activation via email link

    # Authentication URLs
    path('login/', views.loginPage, name="login"),
    # Directs users to the login page

    path('logout/', views.logoutUser, name="logout"),
    # Logs out the user and redirects to the homepage

    path('register/', views.registerPage, name="register"),
    # Directs users to the registration page where they can create an account

    # Home Page URL
    path('', views.home, name="home"),
    # The main home page where users can view rooms, messages, and topics

    # Room URLs
    path('room/<str:pk>/', views.room, name="room"),
    # View for a specific chat room identified by its primary key (pk)

    # User Profile URL
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    # View for user profile page where a user's rooms, messages, and activity are displayed

    # Room Management URLs
    path('create-room/', views.createRoom, name="create-room"),
    # Allows users to create a new chat room

    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    # Allows the room host to update details of an existing room (identified by primary key)

    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    # Allows the room host to delete an existing room (identified by primary key)

    # Message Management URLs
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    # Allows users to delete their own message from the room (identified by primary key)

    # User Profile Update URL
    path('update-user/', views.updateUser, name="update-user"),
    # Allows users to update their profile information, such as username, email, or profile picture

    # Topics Page URL
    path('topics/', views.topicsPage, name="topics"),
    # Displays all available topics to browse and select specific discussion topics

    # Activity Page URL
    path('activity/', views.activityPage, name="activity"),
    # Shows the most recent activity from all rooms, including new messages and room creation

    # Password Reset URLs (Django Auth Views)
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    # Page to request a password reset (user provides their email)

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # Confirmation page displayed after the password reset email has been sent

    path('reset_<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # Page where the user sets a new password after clicking the link in their email

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # Confirmation page displayed after the password reset process is complete
]
    
   
'''My todo list'''
    
    # 1. Submit email form
    # 2. Email sent success message
    # 3. link to password reset form in email
    # 4. password successfully changed email
    # 5. View password feature
    # 6. Notification feature to notify when someone replies to your post
    # 7. Add auto logout feature to end session and redirect user to login --see https://pypi.org/project/django-auto-logout/ and https://github.com/bugov/django-auto-logout
    

