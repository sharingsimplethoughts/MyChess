from django.urls import path
from .views import *
app_name="game"
urlpatterns = [
    path('search_by_username',SearchByUserNameView.as_view(),name='g_search_by_username'),
    path('search_by_email',SearchByEmailView.as_view(),name='g_search_by_email'),
    path('search_friend',SearchFriendView.as_view(),name='g_search_friend'),

    path('send_friend_request',SendFriendRequestView.as_view(),name='g_send_friend_request'),
    path('accept_friend_request',AcceptFriendRequestView.as_view(),name='g_accept_friend_request'),
    path('decline_friend_request',DeclineFriendRequest.as_view(),name='g_decline_friend_request'),

    path('send_game_request',SendGameRequestView.as_view(),name='g_invite_friend'),
    path('notification_list',NotificationListView.as_view(),name='g_notification_list'),
    path('friend_invitation_list',FriendInvitationListView.as_view(),name='g_friend_invitation_list'),
    path('accept_game_request',AcceptGameRequestView.as_view(),name='g_accept_game_request'),
    path('decline_game_request',DeclineGameRequest.as_view(),name='g_decline_game_request'),
    path('time_out_hit',TimeOutHitView.as_view(),name='g_time_out_hit'),
    path('get_game_detail/<int:pk>',GetGameDetailView.as_view(),name='g_game_detail'),
    path('multiple_user_detail',GetMultipleUserDetailView.as_view(),name='g_multiple_user_detail'),
    path('get_user_detail_temp/<int:pk>',GetUserDetailTempView.as_view(),name='g_user_detail_temp'),
    
    path('submit_before_game',SubmitBeforeGameView.as_view(),name='g_submit_before_game'),
    #-------------------------------------
    path('submit_game_data',SubmitGameDataView.as_view(),name='g_submit_game_data'),
    path('update_point',UpdatePointView.as_view(),name='g_update_point'),
    path('recent_opponent',RecentOpponentView.as_view(),name='g_search_friend'),
    #-------------------------------------
    path('upload_image_temporary_api',UploadImageTemporaryApiRequiredByAbhishekOnlyView.as_view(),name='g_upload_image_temporary_api'),
    path('ap_api_delete_notification_user/<int:pk>',DeleteNotificationUserView.as_view(),name='g_ap_api_delete_notification_user'),
    path('ap_api_delete_notification_group/<int:pk>',DeleteNotificationGroupView.as_view(),name='g_ap_api_delete_notification_group'),

    path('get_game_duration_list',GameDurationListView.as_view(),name='g_get_game_duration_list'),
    path('delete_game_duration/<int:pk>',GameDurationDeleteView.as_view(),name='g_delete_game_duration'),
    path('block_unblock_game_duration/<int:pk>',GameDurationBlockUnblockView.as_view(),name='g_block_unblock_game_duration'),
]
