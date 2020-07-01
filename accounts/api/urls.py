from django.urls import path
from .views import *

app_name='accounts'

urlpatterns=[
    path('countrycode_list',CountryCodeListView.as_view(),name='countrycode_list'),
    path('register',RegisterUserView.as_view(),name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('forgot_password',ForgotPasswordView.as_view(),name='forgot_password'),
    path('otp_send',OTPSendView.as_view(),name='otp_send'),
    path('otp_verify',OTPVerifyAPIView.as_view(),name='otp_verify'),
    path('pass_reset_email',PasswordResetEmailView.as_view(),name='pass_reset_email'),
    path('verify_email',VerifyEmailView.as_view(),name='verify_email'),
    path('create_profile',CreateProfileView.as_view(),name="create_profile"),
    path('update_skill_level',UpdateSkillLevelView.as_view(),name='update_skill_level'),
    path('get_skill_level_list',GetSkillLevelListView.as_view(),name='get_skill_level_list_view'),

    path('block_unblock_user/<int:pk>',BlockUnblockUser.as_view(),name='block_unblock_user'),

    # path('create_notification_group',CreateNotificationGroup.as_view(),name='create_notification_group'),
    path('delete_notification_group/<int:pk>',DeleteNotificationGroup.as_view(),name='delete_notification_group'),
    path('view_notification_group/<int:pk>',ViewNotificationGroup.as_view(),name='view_notification_group'),

    path('many_user_list',ManyUserListView.as_view(),name='many_user_list'),
    path('get_random_online_user',GetRandomOnlineUserView.as_view(),name='get_random_online_user'),


    path('leaderboard/<int:pk>',LeaderBoardView.as_view(),name='get_leaderboard'),
    path('scoreboard',ScoreboardView.as_view(),name='get_scoreboard'),

    
    path('send_notification',SendNotificationView.as_view(),name='send_notification'),

]
