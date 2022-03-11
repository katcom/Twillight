from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'pamphlet/index.html')

def user_login(request):
    return render(request,'pamphlet/login.html')


def user_logout(request):
    pass

def user_register(request):
    return render(request,'pamphlet/register.html')
