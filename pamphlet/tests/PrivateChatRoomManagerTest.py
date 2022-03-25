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
class PrivateChatRoomManagerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_manager = UserManager()
        cls.room_manager = PrivateChatRoomManager()

        cls.user = user_manager.create(user_custom_name="user",username="user",password="887788uuy")
        cls.friend = user_manager.create(user_custom_name="friend",username="friend",password="885485tghq")
        cls.room = PrivateChatRoom.objects.create(user_1 = cls.user.user,user_2=cls.friend.user)
        cls.accept_request_url='/api/respond-friend-request/'
        cls.make_request_url='/api/make-friend-request/'
    def setUp(self):
        self.client = APIClient()
    def test_room_manager_get_room_name_success(self):
        room_name = self.room_manager.get_or_create(self.user.user.username,self.friend.user.username)
        self.assertEqual(room_name.room_id,self.room.room_id)
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()