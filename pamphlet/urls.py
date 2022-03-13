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
    path('api/login/',api.login,name="api-login"),
    path('api/register/',api.register,name='api-register'),
    path('api/logout/',api.logout,name='api-logout'),
    path('api/get-all-users/',api.get_all_users,name='api-all-users'),
    path('api/search-users/',api.search_users,name='api-all-users'),
    path('api/create-status/',api.create_status,name='create_status'),
    path('api/get-status/<str:user_id>',api.get_status,name="get_status"),
]