import factory

from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
class UserFactory(factory.django.DjangoModelFactory):
    username ='Dan'
    password=make_password('uuii88990')
    class Meta:
        model = User
class FacePamphletUserFactory(factory.django.DjangoModelFactory):
    user_custom_name="Dan Pickyson"
    user = factory.SubFactory(UserFactory)
    class Meta:
        model = FacePamphletUser
class StatusEntryFactory(factory.django.DjangoModelFactory):
    text_content="Hello World. Have a good day!"
    user = factory.SubFactory(UserFactory)
    visibility = Visibility.PUBLIC_VIEW
    class Meta:
        model = StatusEntry
class FriendRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FriendRequestEntry
