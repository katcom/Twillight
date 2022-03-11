
import re
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .model_managers import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import json
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        user_query = {'username':request.POST['username'],'password':request.POST['username']}
        user_serializer = UserSerializer(data=user_query)

        f_user_query = {"user_custom_name":request.POST['user_custom_name'],'user':user_query}
        f_user_serializer=FacePamphletUserSerializer(data=f_user_query)
        if f_user_serializer.is_valid() and user_serializer.is_valid():
            #f_user = f_user_serializer.save()
            manger = UserManager() 
            f_user = manger.create(username=user_query['username'],user_custom_name=f_user_query['user_custom_name'],password=user_query['password'])
            return Response(f_user_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(f_user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']

        user = authenticate(username=user_id,password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response("You account is disabled!",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid Login",status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def logout(request):
    if request.method == 'GET':
        auth_logout(request)
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def search_users(request):
    try:
        keyword = request.GET['keyword']
        print('keyword is ',keyword)
        users = FacePamphletUser.objects.filter(user_custom_name__contains=keyword)
        serializer = UserSearchResult(users,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_users(request):
    try:
        users = FacePamphletUser.objects.all()
        print("num of users:",len(users))
        serializer = UserSearchResult(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)