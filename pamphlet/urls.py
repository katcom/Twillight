from . import views
from django.urls import path
from . import api
from django.contrib.auth.decorators import login_required
urlpatterns = [ 
    path('',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    path('home/',login_required(login_url='/login/')(views.user_home),name='home'),
    path("user/<str:user_id>",views.user_profile,name="user_profile"),
    path('search-users/',views.search_user,name='register'),
    path('friend-request/',views.friend_request,name="friend_request"),
    path('friend-list/',views.friend_list,name="friend_request"),
    path('private-chat-room/<str:friend_id>/',login_required(login_url='/login/')(views.private_chat_room),name='room'),
    path('settings/',login_required(login_url='/login/')(views.user_settings),name='user_settings'),
    path('friends-status/',login_required(login_url='/login/')(views.friends_status),name='friends_status'),

    path('api/login/',api.login,name="api-login"),
    path('api/register/',api.register,name='api-register'),
    path('api/logout/',api.logout,name='api-logout'),
    path('api/get-all-users/',api.get_all_users,name='api-all-users'),
    path('api/search-users/',api.search_users,name='api-all-users'),
    path('api/create-status/',api.create_status,name='create_status'),
    path('api/get-status/<str:user_id>',api.get_profile_status,name="get_status"),
    path('api/make-friend-request/',api.make_friend_request,name="get_status"),
    path('api/respond-friend-request/',api.respond_friend_request,name="respond_friend_request"),
    path('api/get-friends-list/',api.get_friends_list,name="get_friend_list"),
    path('api/get-current-user-status/',api.get_current_user_status,name="get_friend_list"),
    path('api/update-user-settings/',api.update_user_settings,name="update_user_settings"),
    path('api/get-user-avatar/<str:user_id>',api.get_user_avatar,name="get-user-avatar"),
    path('api/get-friends-status/',login_required(login_url='/login/')(api.get_friends_status),name="get-friends-status"),
    path('api/upload-avatar/',login_required(login_url='/login/')(api.upload_avatar),name="get-friends-status"),
    path('api/like-a-post/',login_required(login_url='/login/')(api.like_a_post),name="like_a_post"),
    path('api/dislike-a-post/',login_required(login_url='/login/')(api.dislike_a_post),name="dislike_a_post"),
    path('api/get-notifications/',api.get_notification,name="get notification"),
    path('api/get-friend-requests/',api.get_friend_requests,name="get friend requests"),
    path('api/get-profile/<str:user_id>',api.get_profile,name="get friend requests"),
    path('api/delete-status/',api.delete_status,name="get friend requests"),
    path('api/upload-profile-background-image/',api.upload_profile_background_image,name="upload_profile_background_image"),
    path('api/update-description/',api.update_description,name="update description"),
    path('api/update-status-visibility/',api.update_status_visibility,name="update description")

    # path('<str:room_name>/',login_required(login_url='/login/')(views.room),name='room'),

]