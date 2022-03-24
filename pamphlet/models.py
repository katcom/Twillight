from argparse import ONE_OR_MORE
from distutils.command.upload import upload
from pickle import TRUE
import profile
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid

from pamphlet.utils import getStatusFilePathByUsername,getAvatarFilePathByUsername
# Create your models here.
class FacePamphletUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="face_pamphlet_account")
    user_custom_name = models.CharField(max_length=256,unique=False,blank=False,null=False)
    def __str__(self):
        return self.user.username
    def __unicode__(self):
        return u'%s' % (self.user.username)
    def  delete(self,*args,**kwargs):
        self.user.delete()
        return super(self.__class__,self).delete(*args,**kwargs)

class UserDescription(models.Model):
    user = models.OneToOneField(FacePamphletUser,null=False,on_delete=models.CASCADE)
    description = models.CharField(max_length=256,default="",blank=True)
    def __str__(self):
        return self.description
class UserProfile(models.Model):
    user = models.OneToOneField(FacePamphletUser,null=False,on_delete=models.CASCADE)
    profile = models.FileField(blank=True,null=True)

class Visibility(models.TextChoices):
    PRIVATE_VIEW = 'PRI',_('Private')
    PUBLIC_VIEW = 'PUB',_('Public')
    FRIENDS_ONLY_VIEW = 'FRI',_('Friends Only')

class StatusEntry(models.Model):
    user = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                related_name="status")

    text_content = models.CharField(max_length=1024,
                                blank=True,
                                null=False,
                                default="")

    visibility = models.CharField(max_length=3,
                                blank=True,
                                null=False,
                                choices=Visibility.choices,
                                default=Visibility.PRIVATE_VIEW)

    isDeleted = models.BooleanField(blank=False,
                                null=False,
                                default=False)

    creation_date = models.DateTimeField(auto_now_add=True,
                                blank=True,null=False,
                                editable=False)

    last_edited = models.DateTimeField(auto_now=True,
                                blank=True,
                                null=False)
    def get_user_custom_name(self):
        return FacePamphletUser.objects.get(user=self.user).user_custom_name
    def __str__(self):
        return "user:{},visibility:{},text-content:{}".format(self.user,self.visibility,self.text_content)
class FriendRequestEntry(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="friend_requests")
    target = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    is_accepted=models.BooleanField(null=True,blank=False)
    creation_date = models.DateTimeField(auto_now_add=True,
                                blank=True,null=False,
                                editable=False)
    message = models.CharField(max_length=256,default="",blank=True,null=False,editable=False)

class FriendshipCreationRecord(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True,blank=True,
                                null=False,
                                editable=False)
class UnilateralFriendship(models.Model):
    user = models.ForeignKey(User,
                        on_delete=models.DO_NOTHING,
                        related_name="friends")

    friend = models.ForeignKey(User,
                        on_delete=models.DO_NOTHING)
    creation_record = models.ForeignKey(FriendshipCreationRecord,on_delete=models.DO_NOTHING,null=False)
    def __str__(self):
        return "user:{}, friend:{}, creation_id:{}, creation_date:{}".format(self.user,self.friend,self.creation_record.pk,self.creation_record.creation_date)


class NotificationType(models.TextChoices):
    FRIEND_REQUEST = 'FRI',_('Friend Request')
    SYSTEM_NOTIFICATION = 'SYS',_('System Notification')

    OTHER_MESSAGE = 'OTE',_('Friend Request')

class Notification(models.Model):
    type = models.CharField(max_length=3,blank=False,null=False,choices=NotificationType.choices,default=NotificationType.OTHER_MESSAGE)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='notifications',null=False)
    is_deleted = models.BooleanField(default=False,null=False,blank=False)
    creation_date = models.DateField(auto_now_add=TRUE,null=False,editable=False)
class NotificationContent(models.Model):
    notification  = models.OneToOneField(Notification,on_delete=models.CASCADE,null=False,related_name="body")
    text_content =models.CharField(max_length=128,null=True,blank=False)

class PrivateChatRoom(models.Model):
    user_1 = models.ForeignKey(User,
                        on_delete=models.DO_NOTHING,
                        related_name="private_chat_rooms")
    user_2 = models.ForeignKey(User,
                        on_delete=models.DO_NOTHING)
    room_id = models.UUIDField(default=uuid.uuid4)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_1','user_2'],name="unique user pair"),
            models.UniqueConstraint(fields=['user_2','user_1'],name="unique user pair 2"),
        ]
class StatusEntryImage(models.Model):
    status_entry = models.ForeignKey(StatusEntry,null=False,blank=False,on_delete=models.CASCADE,related_name="images")
    image_file = models.ImageField(blank=True,null=TRUE,upload_to=getStatusFilePathByUsername)
    thumbnail = models.ImageField(null=True)
    description = models.CharField(max_length=128,null=True,blank=True,default="")

class AvatarEntry(models.Model):
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,related_name='avatar')
    avatar_image = models.ImageField(null=True,blank=True,upload_to=getAvatarFilePathByUsername,default="images/defaults/default-avatar-alien.png")

class LikesEntry(models.Model):
    user = models.ForeignKey(User,related_name='likes',on_delete=models.CASCADE)
    status = models.ForeignKey(StatusEntry,related_name='likes',on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True,editable=False,null=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','status'],name="unique like record"),
        ]
    def __str__(self):
        return "user:{},status:{}".format(self.user,self.status)