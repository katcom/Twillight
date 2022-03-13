from django.shortcuts import render

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

    
