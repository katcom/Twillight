
from asyncore import file_wrapper
from datetime import datetime
import re
import pdb; 
from django.forms import ValidationError
from .utils import *
from .forms import StatusEntryImageForm
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .model_managers import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import user_logged_in
import json
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        user_query = {'username':request.POST['user_id'],'password':request.POST['password']}
        user_serializer = UserSerializer(data=user_query)

        f_user_query = {"user_custom_name":request.POST['username'],'user':user_query}
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
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        auth_logout(request)
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def search_users(request):
    try:
        keyword = request.POST['keyword']
        print('keyword is ',keyword)
        users = FacePamphletUser.objects.filter(user_custom_name__contains=keyword)
        serializer = UserSearchResult(users,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_all_users(request):
    try:
        users = FacePamphletUser.objects.all()
        print("num of users:",len(users))
        serializer = UserSearchResult(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_status(request):
    try:
        if not request.user.is_authenticated:
            return Response("Unauthorized! No user logged in!",status=status.HTTP_401_UNAUTHORIZED)
        queryset = request.POST.copy()
        queryset['user'] = request.user.pk
        print(queryset)
        print('files:')
        print(request.FILES)
        print(type(request.FILES))

        
        
        serializer = StatusEntrySerializer(data=queryset)
        if serializer.is_valid():
            status_entry = serializer.save()
            req = request.POST.copy()
            req['status_entry'] =status_entry
            print("status created")
            print(len(request.FILES))
            for key,file in request.FILES.items():
                print('loop:',key)
                req['status_entry']=status_entry
                file_dict = {"image_file":file}
                form = StatusEntryImageForm(req, file_dict)
                print('checkout file')
                if form.is_valid():
                    form.save()
                    print("file created")
                else:
                    print("form err:",form.errors)
                    return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)

                
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_status(request,user_id):
    try:
        status_list = User.objects.get(username=user_id).status
        serializer = StatusGetResultSerializer(status_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def make_friend_request(request):
    try:
        # validate user input, check if user and target exists
        queryset = request.POST.copy()
        user_id=request.user.username
        target_id=queryset.pop('target_id')[0]
        #print(user_id,target_id)
        # if not User.objects.filter(username=user_id).exists():
        #     raise serializers.ValidationError("User with id {} does not exist".format(user_id))
        if not User.objects.filter(username=target_id).exists():
            raise serializers.ValidationError("User with id {} does not exist".format(target_id))
        
        queryset['user'] = User.objects.get(username=user_id).pk
        queryset['target'] = User.objects.get(username=target_id).pk


        serializer = FriendRequestSourceSerializer(data=queryset)

        if(serializer.is_valid()):
            record = serializer.create(serializer.validated_data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(json.dumps(str(e)),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def respond_friend_request(request):
    try:
        #print('CALLED')

        record = FriendRequestEntry.objects.get(pk=request.POST["record_id"])
        serializer = FriendRequestResponseSerializer(record,data={"is_accepted":request.POST["is_accepted"]},partial=True)
        if serializer.is_valid():
            new_record = serializer.save()
            #print(new_record.user)

            if new_record.is_accepted:
                manager = FriendshipManager()
                manager.create(request.user,new_record.user)

            #print('updated')
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_friends_list(request):
    try:
        friends_record_list = ValidUnilateralFriendship.objects.filter(friendship__user=request.user)
        friends_list = []
        for entry in friends_record_list:
            friend =  FacePamphletUser.objects.get(user=entry.friendship.friend)
            friends_list.append(friend)
        serializer = FriendSerializer(friends_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def get_friends_list(request):
#     try:
#         friends_record_list = ValidUnilateralFriendship.objects.filter(friendship__user=request.user)
#         friends_list = []
#         for entry in friends_record_list:
#             friend =  FacePamphletUser.objects.get(user=entry.friendship.friend)
#             friends_list.append(friend)
#         serializer = FriendSerializer(friends_list,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     except:
#         return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_current_user_status(request):
    if not request.user.is_authenticated:
        return Response("Unauthorized! No user logged in!",status=status.HTTP_401_UNAUTHORIZED)
    try:

        record = StatusEntry.objects.filter(user=request.user,isDeleted=False);
        serializer = CurrentUserStatusSerializer(record,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e :
        return Response(json.dumps(str(e)),status=status.HTTP_400_BAD_REQUEST)