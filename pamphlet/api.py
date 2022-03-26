
from asyncore import file_wrapper
from datetime import datetime
from multiprocessing import managers
import re
import pdb; 
from django.forms import ValidationError
from .utils import *
from .forms import *
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
    try:
        if request.method == 'POST':
            user_query = {'username':request.POST['user_id'],'password':request.POST['password']}
            user_serializer = UserSerializer(data=user_query)

            f_user_query = {"user_custom_name":request.POST['username'],'user':user_query}
            f_user_serializer=FacePamphletUserSerializer(data=f_user_query)
            if f_user_serializer.is_valid() and user_serializer.is_valid():
                #f_user = f_user_serializer.save()
                manger = UserManager() 
                f_user = manger.create(username=user_query['username'],user_custom_name=f_user_query['user_custom_name'],password=user_query['password'])
                AvatarEntry.objects.create(user=f_user.user)
                ProfileEntry.objects.create(user=f_user.user)
                UserDescription.objects.create(user=f_user.user)
                return Response(f_user_serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(f_user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_500-INTERNAL_SERVER_ERROR)
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
        # print(queryset)
        # print('files:')
        # print(request.FILES)
        # print(type(request.FILES))

        
        
        serializer = StatusEntrySerializer(data=queryset)
        if serializer.is_valid():
            status_entry = serializer.save()
            req = request.POST.copy()
            req['status_entry'] =status_entry
            # print("status created")
            # print(len(request.FILES))
            for key,file in request.FILES.items():
                req['status_entry']=status_entry
                file_dict = {"image_file":file}
                form = StatusEntryImageForm(req, file_dict)
                if form.is_valid():
                    form.save()
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
def get_profile_status(request,user_id):
    try:
        status_list = User.objects.get(username=user_id).status.filter(visibility=Visibility.PUBLIC_VIEW)
        serializer = UserStatusSerializer(status_list,many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
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
        print('CALLED')
        print('DATA:',request.POST)
        record = FriendRequestEntry.objects.get(pk=request.POST["record_id"])
        print('record -get')

        serializer = FriendRequestResponseSerializer(record,data={"is_accepted":request.POST["is_accepted"]},partial=True)
        if serializer.is_valid():
            print('valid form')

            new_record = serializer.save()
            #print(new_record.user)

            if new_record.is_accepted:
                manager = FriendshipManager()
                manager.create(request.user,new_record.user)

            #print('updated')
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            print('invalid form')
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_friends_list(request):
    try:
        friends_record_list = UnilateralFriendship.objects.filter(user=request.user)
        friends_list = []
        for entry in friends_record_list:
            friend =  FacePamphletUser.objects.get(user=entry.friend)
            friends_list.append(friend)
        serializer = FriendSerializer(friends_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
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

        record = StatusEntry.objects.filter(user=request.user,isDeleted=False).order_by('-last_edited');
        serializer = CurrentUserStatusSerializer(record,many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e :
        return Response(json.dumps(str(e)),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_user_settings(request):
    # queryset = request.POST.copy()
    # queryset['user_id'] = request.user.username 
    form = UserSettingForm(request.POST,instance=request.user.face_pamphlet_account)
    if form.is_valid():
        form.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_avatar(request,user_id):
    user = User.objects.filter(username=user_id)
    if not user:
        return Response("ERROR! User does not exist!!",status=status.HTTP_400_BAD_REQUEST)
    img_url = user[0].avatar.avatar_image.url
    data_dict = {'url':img_url}
    return Response(data_dict,status=status.HTTP_200_OK)

@api_view(['GET'])
def get_friends_status(request):
    try:
        manager = FriendshipManager()
        friends=manager.get_mutual_friends(user=request.user)
        #print(friends)
        record = StatusEntry.objects.filter(user__in=friends,isDeleted=False,visibility__in=[Visibility.FRIENDS_ONLY_VIEW,Visibility.PUBLIC_VIEW]).order_by('-creation_date');
        serializer = UserStatusSerializer(record,many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e :
        print(e)
        return Response(json.dumps(str(e)),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def upload_avatar(request):
    form = AvatarForm(request.POST,request.FILES,instance=request.user.avatar)
    #print(request.FILES)
    if form.is_valid():
        form.save()
        return Response(status=status.HTTP_200_OK)
    return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def like_a_post(request):
    try:
        print(request.POST)
        form = LikeEntryForm(request.POST)
        if form.is_valid():
            raw_like_entry = form.save(commit=False)

            if LikesEntry.objects.filter(user=request.user.pk,status=raw_like_entry.status).exists():
                print('already liked')
                return Response('User {} already liked this post'.format(raw_like_entry.user),status=status.HTTP_400_BAD_REQUEST)
            else:
                raw_like_entry.user = request.user;
                print('raw_like_entry:',raw_like_entry)

                raw_like_entry.save()
                form.save()
                return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def dislike_a_post(request):
    try:
        print('try')
        form = LikeEntryForm(request.POST)
        raw_like_entry = form.save(commit=False)
        entry = LikesEntry.objects.filter(user=request.user.pk,status=raw_like_entry.status);
        if not entry.exists():
            return Response('User has not liked this post before',status=status.HTTP_400_BAD_REQUEST)
        else:
            entry[0].delete()
            return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_notification(request):
    try:
        if not request.user.is_authenticated:
            return  Response(status=status.HTTP_401_UNAUTHORIZED)
        entries = Notification.objects.filter(user=request.user,is_deleted=False)
        serializer = NotificationSerializer(entries,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_friend_requests(request):
    try:
        if not request.user.is_authenticated:
            return  Response(status=status.HTTP_401_UNAUTHORIZED)
        friend_req_list = FriendRequestEntry.objects.filter(target=request.user)
        serializer = FriendRequestTargetSerializer(friend_req_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_profile(request,user_id):
    try:
        profile = FacePamphletUser.objects.get(user__username=user_id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def delete_status(request):
    try:
        if not request.user.is_authenticated:
            return  Response(status=status.HTTP_401_UNAUTHORIZED)

        status_entry = StatusEntry.objects.get(pk=request.POST['pk'])
            # status_entry = status_serializer.save()
            # print(status_entry)
            # if the post does not belong to the current user,return 401 error
        if status_entry.user != request.user:
            return  Response(status=status.HTTP_401_UNAUTHORIZED)

        status_entry.delete()
        return Response('Status Deleted',status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def upload_profile_background_image(request):
    if not request.user.is_authenticated:
        return  Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        form = ProfileBackgroundImageForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            img = form.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response('Invalid data',status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_description(request):
    if not request.user.is_authenticated:
        return  Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        form = DescriptionForm(request.POST,instance=request.user.description)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response('Invalid data',status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_status_visibility(request):
    if not request.user.is_authenticated:
        return  Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        serializer = ChangeStatusVisibilitySerializer(data=request.POST)
        if serializer.is_valid():
            # print('is valid')
            # print('data',serializer.data)
            # if the post does not belong to the current user,return 401 error
            status_entry = StatusEntry.objects.get(pk=request.POST['pk'])
              
            if status_entry.user != request.user:
                return  Response(status=status.HTTP_401_UNAUTHORIZED)
            
            status_entry.visibility = serializer.data['visibility']
            status_entry.save()
            return Response(status=status.HTTP_200_OK) 
        else:
            return Response('Invalid data',status=status.HTTP_400_BAD_REQUEST)


    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

