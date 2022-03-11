from . import views
from django.urls import path
from . import api
urlpatterns = [ 
    path('',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    path('api/login/',api.login,name="api-login"),
    path('api/register/',api.register,name='api-register'),
    path('api/logout/',api.logout,name='api-logout'),
    path('api/get-all-users/',api.get_all_users,name='api-all-users'),
    path('api/search-users/',api.search_users,name='api-all-users'),

]