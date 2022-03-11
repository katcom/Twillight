from django.forms import CharField
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
class FacePamphletUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = FacePamphletUser
        fields = ['user_custom_name','user']
    
    def create(self,validated_data):
        # user = User.objects.get(username=self.initial_data['username'])
        # f_user = FacePamphletUser(**{**validated_data,
        #     'user':user
        # })
        # f_user.save()
        # user_dict =validated_data.pop('user')
        # user = User.objects.create(**user_dict)
        # f_user = FacePamphletUser.objects.create(user=user,**validated_data)
        # return f_user
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        f_user = FacePamphletUser.objects.create(user=user, **validated_data)

        return f_user

class UserSearchResult(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.username')
    class Meta:
        model = FacePamphletUser
        fields = ['user_custom_name','user_id']