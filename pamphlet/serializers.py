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
    
    # def create(self,validated_data):
    #     # user = User.objects.get(username=self.initial_data['username'])
    #     # f_user = FacePamphletUser(**{**validated_data,
    #     #     'user':user
    #     # })
    #     # f_user.save()
    #     # user_dict =validated_data.pop('user')
    #     # user = User.objects.create(**user_dict)
    #     # f_user = FacePamphletUser.objects.create(user=user,**validated_data)
    #     # return f_user
    #     user_data = validated_data.pop('user')
    #     user = User.objects.create(**user_data)
    #     f_user = FacePamphletUser.objects.create(user=user, **validated_data)

    #     return f_user

class UserSearchResult(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.username')
    class Meta:
        model = FacePamphletUser
        fields = ['user_custom_name','user_id']


class UserCustomNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacePamphletUser
        fields = ['user_custom_name']

class StatusEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusEntry
        fields = ['user','text_content','visibility']

class ProfileStatusSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.username')
    class Meta:
        model = StatusEntry
        fields = ['pk','user_id','text_content','visibility','creation_date','creation_date','last_edited']

class FriendRequestTargetSerializer(serializers.ModelSerializer):
    user_custom_name = serializers.CharField(source='user.face_pamphlet_account.user_custom_name')
    user_id = serializers.CharField(source='user.username')
    is_undetermined = serializers.SerializerMethodField('get_is_determined')
    def get_is_determined(self,instance):
        if instance.is_accepted is None:
            return True
        return False
    class Meta:
        model = FriendRequestEntry
        fields=['pk','user','user_custom_name',"user_id",'is_accepted','is_undetermined']
class FriendRequestSourceSerializer(serializers.ModelSerializer):
    # user_id = serializers.CharField(source='user.username',read_only=True)
    # target_id = serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model = FriendRequestEntry
        fields=['user','target']

class FriendRequestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequestEntry
        fields=['is_accepted']

class FriendSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.username')
    class Meta:
        model = FacePamphletUser
        fields=['user_id','user_custom_name']
class StatusEntryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusEntryImage
        fields=['image_file','description']
class CurrentUserStatusSerializer(serializers.ModelSerializer):
    images = StatusEntryImageSerializer(many=True,read_only=True)
    user_id = serializers.CharField(source='user.username')
    user_custom_name = serializers.CharField(source='get_user_custom_name')
    likes_num = serializers.SerializerMethodField('get_likes_num')
    is_liked = serializers.SerializerMethodField('get_is_liked')

    def get_likes_num(self, instance):
        return instance.likes.all().count()
    def get_is_liked(self,instance):
        request = self.context['request']
        if not request.user.is_authenticated:
            return False
        return instance.likes.filter(user=request.user).exists()
    class Meta:
        model=StatusEntry
        fields=['pk','user_id','user_custom_name','text_content','visibility','creation_date','last_edited','images','likes_num','is_liked']

class UserStatusSerializer(serializers.ModelSerializer):
    images = StatusEntryImageSerializer(many=True,read_only=True)
    user_id = serializers.CharField(source='user.username')
    user_custom_name = serializers.CharField(source='get_user_custom_name')
    is_liked = serializers.SerializerMethodField('get_is_liked')
    def get_is_liked(self,instance):
        request = self.context['request']
        if not request.user.is_authenticated:
            return False
        return instance.likes.filter(user=request.user).exists()
    class Meta:
        model=StatusEntry
        fields=['pk','user_id','user_custom_name','text_content','visibility','creation_date','last_edited','images','is_liked']

class NotificationSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='body.text_content')
    class Meta:
        model = Notification
        fields=['type','creation_date','content']

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.username')
    profile = serializers.SerializerMethodField('get_profile')
    description = serializers.CharField(source='user.description.description')
    avatar = serializers.CharField(source='user.avatar.avatar_image.url')
    def get_profile(self,instance):
        img = instance.user.profile.background_image
        if img:
            return img.url
        return None
    class Meta:
        model = FacePamphletUser
        fields = ['user_id','user_custom_name','profile','description','avatar']


class StatusDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusEntry
        fields=['pk',]

class ChangeStatusVisibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusEntry
        fields=['pk','visibility']