from django.forms import CharField
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.password_validation import validate_password
from . import utils
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
    def validate_password(self,value):
        validate_password(password=value)
        if len(value) < 8:
            raise serializers.ValidationError('Password should be at least 8 characters long')
        
        
        if not utils.hasLetterInString(value):
            raise serializers.ValidationError('Password should cotain at least one letter')
        
        if not utils.hasNumberInString(value):
            raise serializers.ValidationError('Password should cotain at least one number')

        

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

class StatusEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusEntry
        fields = ['user','text_content','visibility']

class StatusGetResultSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.username')
    class Meta:
        model = StatusEntry
        fields = ['user_id','text_content','visibility','creation_date','creation_date','last_edited']