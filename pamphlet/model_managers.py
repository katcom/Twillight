from datetime import datetime
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import *
from django.contrib.auth.hashers import make_password
class UserManager(models.Manager):
    def create(self,username,user_custom_name,password):
        try:
            user = User(username=username,password=make_password(password))
            user.save()

            face_pamphlet_user = FacePamphletUser(user=user,user_custom_name=user_custom_name)
            face_pamphlet_user.save()
            return face_pamphlet_user 
        except:
            raise Exception("Something Wrong in UserManager")

class FriendshipManager(models.Manager):
    def create(self,user_1,user_2):
        if UnilateralFriendship.objects.filter(user=user_1,friend = user_2).exists() or \
                UnilateralFriendship.objects.filter(user=user_2,friend=user_1).exists():
            raise ValidationError("{} is already a friend of {}".format(user_1,user_2))
        creation_record = FriendshipCreationRecord.objects.create()
        friendship_me_to_friend = UnilateralFriendship.objects.create(user=user_1,friend=user_2,creation_record=creation_record)
        friendship_friend_to_me = UnilateralFriendship.objects.create(user=user_2,friend=user_1,creation_record=creation_record)
    def get_mutual_friends(self,user):
        friends=[]
        friendships = UnilateralFriendship.objects.filter(user=user)
        for friendship in friendships:
            if UnilateralFriendship.objects.filter(user=friendship.friend,friend=user).exists():
                friends.append(friendship.friend)
        return friends
class PrivateChatRoomManager(models.Manager):
    def create(self,user_1,user_2):
        user1 = User.objects.filter(username=user_1)
        if not user1:
            raise ValidationError('User {} does not exist!'.format(user_1))
        user1 =user1[0]

        user2 = User.objects.filter(username=user_2)
        if not user2:
            raise ValidationError('User {} does not exist!'.format(user_2))
        user2 = user2[0]
        if PrivateChatRoom.objects.filter(user_1__username=user_1,user_2__username=user_2).exists() or \
            PrivateChatRoom.objects.filter(user_2__username=user_1,user_1__username=user_2).exists():
            raise ValidationError('Private Chatroom already exists for users {} and {}!'.format(user_1,user_2))

        room = PrivateChatRoom.objects.create(user_1=user1,user_2=user2)
        return room
    def get_or_create(self,user_1_name,user_2_name):
        room = PrivateChatRoom.objects.filter(user_1__username=user_1_name,user_2__username=user_2_name)
        if not room:
            room= PrivateChatRoom.objects.filter(user_2__username=user_1_name,user_1__username=user_2_name)

        if not room:
            return self.create(user_1_name,user_2_name)
        return room[0]