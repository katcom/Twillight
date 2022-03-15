from argparse import ONE_OR_MORE
from pickle import TRUE
import profile
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class FacePamphletUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
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

class FriendRequestEntry(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="friends")
    friend = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    is_accepted=models.BooleanField(null=True,blank=False)
    creation_date = models.DateTimeField(auto_now_add=True,
                                blank=True,null=False,
                                editable=False)
    is_deleted = models.BooleanField(default=False,null=True)

# class NotificationType(models.TextChoices):
#     FRIEND_REQUEST = 'FRI',_('Friend Request')
#     OTHER_MESSAGE = 'OTE',_('Friend Request')

# class Notification(models.Model):
#     type = models.CharField(max_length=3,blank=False,null=False,choices=NotificationType.choices,default=NotificationType.OTHER_MESSAGE)
