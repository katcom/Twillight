import json
import os
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from pamphlet.models import FacePamphletUser
from pamphlet.model_managers import *
from pamphlet.model_factories import *
from datetime import *

class LikesPostTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_manager = UserManager()
        cls.url='/api/like-a-post/'

        cls.friendship_manager = FriendshipManager()
        cls.user = cls.user_manager.create(user_custom_name="user",username="unittest_user",password="887788uuy")
        cls.friend_1 = cls.user_manager.create(user_custom_name="friend",username="unittest_friend",password="885485tghq")
        cls.status_user_1_pub = StatusEntryFactory(user=cls.user.user,visibility=Visibility.PUBLIC_VIEW)
        cls.status_friend_1_PUB = StatusEntryFactory(user=cls.friend_1.user,visibility=Visibility.PUBLIC_VIEW)
        cls.friendship_manager.create(cls.user.user,cls.friend_1.user)
    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.user.user)
    def test_like_a_post_success(self):
        valid_data={"status":self.status_friend_1_PUB.pk}
        response = self.client.post(self.url,valid_data)
        self.assertEqual(response.status_code,200)
    def test_like_a_post_success_and_like_entry_exists(self):
        valid_data={"status":self.status_friend_1_PUB.pk}
        response = self.client.post(self.url,valid_data)
        entry = LikesEntry.objects.filter(user=self.user.user.pk,status=self.status_friend_1_PUB)
        self.assertTrue(entry.exists())
    def test_like_a_post_success_and_like_entry_with_correct_user(self):
        valid_data={"status":self.status_friend_1_PUB.pk}
        response = self.client.post(self.url,valid_data)
        entries = LikesEntry.objects.filter(user=self.user.user.pk,status=self.status_friend_1_PUB)
        entry=entries[0]
        self.assertEqual(entry.user,self.user.user)
    def test_like_a_post_success_and_like_entry_with_correct_status(self):
        valid_data={"status":self.status_friend_1_PUB.pk}
        response = self.client.post(self.url,valid_data)
        entries = LikesEntry.objects.filter(user=self.user.user.pk,status=self.status_friend_1_PUB)
        entry=entries[0]
        self.assertEqual(entry.status,self.status_friend_1_PUB)
    def test_like_a_post_failed_on_no_like_record_found(self):
        valid_data={"status":self.status_friend_1_PUB.pk}
        response = self.client.post(self.url,valid_data)
        entry = LikesEntry.objects.filter(user=self.user.user.pk,status=self.status_user_1_pub)
        #print(entry.exists())
        self.assertFalse(entry.exists())
    def test_image_is_returned(self):
        pass
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

class DislikesPostTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_manager = UserManager()
        cls.url='/api/dislike-a-post/'

        cls.friendship_manager = FriendshipManager()
        cls.user = cls.user_manager.create(user_custom_name="user",username="unittest_user",password="887788uuy")
        cls.friend_1 = cls.user_manager.create(user_custom_name="friend",username="unittest_friend",password="885485tghq")
        cls.status_user_1_pub = StatusEntryFactory(user=cls.user.user,visibility=Visibility.PUBLIC_VIEW)
        cls.status_friend_1_PUB = StatusEntryFactory(user=cls.friend_1.user,visibility=Visibility.PUBLIC_VIEW)
        cls.friendship_manager.create(cls.user.user,cls.friend_1.user)
    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.user.user)
        self.like_entry = LikesEntry.objects.create(user=self.user.user,status=self.status_friend_1_PUB)

    def test_dislike_a_post_success(self):
        valid_data={"status":self.status_friend_1_PUB.pk}
        response = self.client.post(self.url,valid_data)
        self.assertEqual(response.status_code,200)
    def test_dislike_a_post_success_and_like_entry_is_removed(self):
        valid_data={"status":self.status_friend_1_PUB.pk}
        response = self.client.post(self.url,valid_data)
        entry = LikesEntry.objects.filter(user=self.user.user,status=self.status_friend_1_PUB)
        #print(entry)
        self.assertFalse(entry.exists())
    def test_dislike_a_post_failed_on_non_exist_record(self):
        valid_data={"status":self.status_user_1_pub.pk}
        response = self.client.post(self.url,valid_data)
        self.assertEqual(response.status_code,400)
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()