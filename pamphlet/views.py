from django.shortcuts import render

from pamphlet.forms import AvatarForm, UserSettingForm

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
    profile = FacePamphletUser.objects.get(user__username=user_id)
    serializer = UserProfileSerializer(profile)
    return render(request,'pamphlet/user_profile.html',{"profile":serializer.data})

def friend_request(request):
    friend_req_list = FriendRequestEntry.objects.filter(target=request.user)
    return render(request,'pamphlet/notification.html',{"request_list":friend_req_list})

def friend_list(request):
    return render(request,'pamphlet/friends.html')

def private_chat_room(request,friend_id):
    try:
        manager = PrivateChatRoomManager()
        room = manager.get_or_create(request.user.username,friend_id)

        return render(request,'pamphlet/room.html',{
                    'room_name':str(room.room_id),
                    'friend_name':str(FacePamphletUser.objects.get(user__username=friend_id).user_custom_name)
        })
    except Exception as e:
        print('err:',e)

def user_settings(request):
    avatar_form = AvatarForm()
    fp_user = FacePamphletUser.objects.get(user=request.user)
    form = UserSettingForm(instance=fp_user)
    return render(request,'pamphlet/settings.html',{'form':form,'fp_user':fp_user,'avatar_form':avatar_form})

def friends_status(request):
    return render(request,'pamphlet/friends_status.html')