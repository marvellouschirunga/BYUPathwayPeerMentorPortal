from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home" ),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset_<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    
   

    
    # 1. Submit email form
    # 2. Email sent success message
    # 3. link to password reset form in email
    # 4. password successfully changed email
    # 5. View password feature
    # 6. Notification feature to notify when someone replies to your post
    # 7. Add auto logout feature to end session and redirect user to login --see https://pypi.org/project/django-auto-logout/ and https://github.com/bugov/django-auto-logout
    

]