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
import shutil
class FriendStatusTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_manager = UserManager()

        cls.friendship_manager = FriendshipManager()
        cls.user = cls.user_manager.create(user_custom_name="user",username="unittest_user",password="887788uuy")
        cls.friend_1 = cls.user_manager.create(user_custom_name="friend",username="unittest_friend",password="885485tghq")
        cls.friend_2 = cls.user_manager.create(user_custom_name="friend",username="unittest_friend_2",password="885485tghq")
        cls.stranger = cls.user_manager.create(user_custom_name="friend",username="unittest_stranger",password="885485tghq")
        cls.status_user_1_pub = StatusEntryFactory(user=cls.user.user,visibility=Visibility.PUBLIC_VIEW)
        cls.status_friend_1_PUB = StatusEntryFactory(user=cls.friend_1.user,visibility=Visibility.PUBLIC_VIEW)
        cls.status_friend_1_FRI = StatusEntryFactory(user=cls.friend_2.user,visibility=Visibility.FRIENDS_ONLY_VIEW)
        cls.status_friend_1_PRI = StatusEntryFactory(user=cls.friend_2.user,visibility=Visibility.PRIVATE_VIEW)
        cls.status_friend_2_pub = StatusEntryFactory(user=cls.friend_2.user,visibility=Visibility.PUBLIC_VIEW)
        cls.status_stranger_pub = StatusEntryFactory(user=cls.stranger.user,visibility=Visibility.PUBLIC_VIEW)

        cls.status_image = StatusImageFactory(status_entry=cls.status_friend_1_FRI)
        cls.friendship_manager.create(cls.user.user,cls.friend_1.user)
        cls.friendship_manager.create(cls.user.user,cls.friend_2.user)
    def setUp(self):
        self.client = APIClient()
        self.url='/api/get-friends-status/'
        self.client.force_login(self.user.user)
    def test_get_friend_status_success(self):
        print(self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
    def test_has_all_status_got(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        print(data)
        self.assertEqual(len(data),3)
    def test_user_id_is_returned(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertIn(data[0]['user_id'],[self.friend_1.user.username,self.friend_2.user.username])
    def test_user_custom_name_is_returned(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertIn(data[0]['user_custom_name'],[self.friend_1.user_custom_name,self.friend_2.user_custom_name])
    def test_user_text_content_is_returned(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertIn(data[0]['text_content'],[self.status_friend_1_PUB.text_content,self.status_friend_1_FRI.text_content,self.status_friend_2_pub.text_content])
    def test_user_visibility_is_returned(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertIn(data[0]['visibility'],['PRI','FRI','PUB'])
    def test_creation_date_is_returned(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertIsNotNone(data[0]['creation_date'])
    def test_last_edited_is_returned(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertIsNotNone(data[0]['last_edited'])
    def test_private_status_is_not_returned(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertNotIn(self.status_friend_1_PRI.pk,[e['pk'] for e in data])
    def test_strangers_status_is_not_returned(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertNotIn(self.status_stranger_pub.pk,[e['pk'] for e in data])
    def test_image_is_returned(self):
        pass
    @classmethod
    def tearDownClass(cls):
        directory='UserAppData//'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if filename.startswith('unittest') and os.path.isdir(f):
                # checking if it is a file
                print('remove test data:',f)
                shutil.rmtree(f)
        super().tearDownClass()