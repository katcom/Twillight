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

    path('api/login/',api.login,name="api-login"),
    path('api/register/',api.register,name='api-register'),
    path('api/logout/',api.logout,name='api-logout'),
    path('api/get-all-users/',api.get_all_users,name='api-all-users'),
    path('api/search-users/',api.search_users,name='api-all-users'),
    path('api/create-status/',api.create_status,name='create_status'),
    path('api/get-status/<str:user_id>',api.get_status,name="get_status"),
    path('api/make-friend-request/',api.make_friend_request,name="get_status"),
    path('api/respond-friend-request/',api.respond_friend_request,name="respond_friend_request"),
    path('api/get-friends-list/',api.get_friends_list,name="get_friend_list"),
    path('api/get-current-user-status/',api.get_current_user_status,name="get_friend_list"),

    # path('<str:room_name>/',login_required(login_url='/login/')(views.room),name='room'),
    path('private-chat-room/<str:friend_id>/',login_required(login_url='/login/')(views.private_chat_room),name='room'),

]