from django.shortcuts import render

from .serializers import *
from .model_managers import *
from .models import *
# Create your views here.
def index(request):
    status=[]
    f_user =None
    if request.user.is_authenticated:
        print(request.user)
        status = request.user.status.all()
        f_user = FacePamphletUser.objects.get(user=request.user)
    return render(request,'pamphlet/index.html',{'status_list':status,'f_user':f_user})

def user_login(request):
    return render(request,'pamphlet/login.html')


def user_logout(request):
    pass

def user_register(request):
    return render(request,'pamphlet/register.html')

def search_user(request):
    return render(request,'pamphlet/search.html')

def user_home(request):
    status = request.user.status.all()
    return render(request,'pamphlet/user_home.html',{"status_list":status,'f_user':FacePamphletUser.objects.get(user=request.user)})

def user_profile(request,user_id):
    return render(request,'pamphlet/user_profile.html',{"user_id":user_id})

def friend_request(request):
    friend_req_list = FriendRequestEntry.objects.filter(target=request.user)
    return render(request,'pamphlet/notification.html',{"request_list":friend_req_list})

def friend_list(request):
    # friends_record_list = UnilateralFriendshipRecord.objects.filter(is_deleted=False)
    # friends_list = []
    # for entry in friends_record_list:
    #     friend =  FacePamphletUser.objects.get(user=entry.friendship.friend)
    #     friends_list.append(friend)
    # serializer = FriendSerializer(friends_list,many=True)
    # print(serializer.data)
    return render(request,'pamphlet/friends_status.html')

def private_chat_room(request,friend_id):
    try:
        manager = PrivateChatRoomManager()
        room = manager.get_or_create(request.user.username,friend_id)

        return render(request,'pamphlet/room.html',{
                    'room_name':str(room.room_id)
        })
    except Exception as e:
        print('err:',e)