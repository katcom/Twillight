import json
import os
from urllib import request, response
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from pamphlet.models import FacePamphletUser
from pamphlet.model_managers import *
from pamphlet.model_factories import *
from datetime import *
import time
class MakeAndAcceptFriendRequestIntegration(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mangaer = UserManager()

        cls.user = mangaer.create(user_custom_name="user",username="user",password="887788uuy")
        cls.friend = mangaer.create(user_custom_name="friend",username="friend",password="885485tghq")
        cls.accept_request_url='/api/respond-friend-request/'
        cls.make_request_url='/api/make-friend-request/'
    def setUp(self):
        self.client = APIClient()
    def test_make_and_accept_friend_request_success(self):
        self.client.force_login(self.user.user)
        valid_request_data = {"target_id":"friend"} 
        self.client.post(self.make_request_url,valid_request_data)
        self.client.logout()
        self.client.force_login(self.friend.user)
        valid_accept_data = {"record_id":"1","is_accepted":"True"} 
        self.client.post(self.accept_request_url,valid_accept_data)
        friend_record = UnilateralFriendship.objects.get(user=self.user.user,friend=self.friend.user)
        #print(friend_record) 
        self.assertIsNotNone(friend_record)
        friend_record = UnilateralFriendship.objects.get(user=self.friend.user,friend=self.user.user)
        #print(friend_record) 
        self.assertIsNotNone(friend_record)
    def test_make_and_reject_friend_request_success(self):
        self.client.force_login(self.user.user)
        valid_request_data = {"target_id":"friend"} 
        self.client.post(self.make_request_url,valid_request_data)
        self.client.logout()
        self.client.force_login(self.friend.user)
        valid_accept_data = {"record_id":"1","is_accepted":"False"} 
        self.client.post(self.accept_request_url,valid_accept_data)
        has_user = UnilateralFriendship.objects.filter(user=self.user.user,friend=self.friend.user).exists()
        #print(friend_record) 
        self.assertFalse(has_user)
        has_friend = UnilateralFriendship.objects.filter(user=self.friend.user,friend=self.user.user).exists()
        #print(friend_record) 
        self.assertFalse(has_friend)