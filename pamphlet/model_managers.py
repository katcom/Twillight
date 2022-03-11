from django.db import models
from django.contrib.auth.models import User
from .models import *

class UserManager(models.Manager):
    def create(self,username,user_custom_name,password):
        try:
            user = User(username=username,password=password)
            user.save()

            face_pamphlet_user = FacePamphletUser(user=user,user_custom_name=user_custom_name)
            face_pamphlet_user.save()
            return face_pamphlet_user 
        except:
            raise Exception("Something Wrong in UserManager")
