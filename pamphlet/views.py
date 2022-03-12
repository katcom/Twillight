from django.shortcuts import render

# Create your views here.
def index(request):
    status=[]
    if request.user.is_authenticated:
        print(request.user)
        status = request.user.status.all()
    return render(request,'pamphlet/index.html',{'status_list':status})

def user_login(request):
    return render(request,'pamphlet/login.html')


def user_logout(request):
    pass

def user_register(request):
    return render(request,'pamphlet/register.html')

def search_user(request):
    return render(request,'pamphlet/search.html')

def user_home(request):
    return render(request,'pamphlet/userhome.html')