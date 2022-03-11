import profile
from django.db import models
from django.contrib.auth.models import User


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