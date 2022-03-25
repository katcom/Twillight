
import json
import os
from pydoc import resolve
from urllib import request, response
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from pamphlet.models import FacePamphletUser
from pamphlet.model_managers import *
from pamphlet.model_factories import *
from datetime import *
class FriendRequestTest(APITestCase):
    def setUp(self) -> None:
        mangaer = UserManager()
        self.user = mangaer.create(user_custom_name="user",username="user",password="887788uuy")
        self.friend = mangaer.create(user_custom_name="friend",username="friend",password="885485tghq")
        self.url='/api/make-friend-request/'
        self.client = APIClient()
        self.client.force_login(self.user.user)
        self.url_respond_request='/api/respond-friend-request/'
    def test_create_friend_request_success(self):
        valid_request_data = {"target_id":"friend"} 
        response = self.client.post(self.url,valid_request_data)
        #print(response.content)
        self.assertEqual(response.status_code,201)
    # def test_create_friend_request_failed_on_invalid_user_id(self):
    #     valid_request_data = {"user_id":"xxxxx","target_id":"friend"} 
    #     response = self.client.post(self.url,valid_request_data)
    #     #print(response.content)
    #     self.assertEqual(response.status_code,400)
    def test_create_friend_request_failed_on_invalid_target_id(self):
        valid_request_data = {"target_id":"xxxxxx"} 
        response = self.client.post(self.url,valid_request_data)
        #print(response.content)
        self.assertEqual(response.status_code,400)

class FriendRequestRespondTest(APITestCase):
    def setUp(self) -> None:
        mangaer = UserManager()
        self.user = mangaer.create(user_custom_name="user",username="user",password="887788uuy")
        self.friend = mangaer.create(user_custom_name="friend",username="friend",password="885485tghq")
        #self.friend = mangaer.create(user_custom_name="third_guy",username="third_guy",password="885485tghq")

        self.client = APIClient()
        self.client.force_login(self.user.user)
        self.url='/api/respond-friend-request/'
    def test_respond_friend_request_success(self):
        freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
        response = self.client.post(self.url,valid_request_data)
        self.assertEqual(response.status_code,200)
    def test_respond_friend_request_success_accept_has_database_changed(self):
        freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
        response = self.client.post(self.url,valid_request_data)
        self.assertEqual(FriendRequestEntry.objects.get(pk=freq.pk).is_accepted,True)
    def test_respond_friend_request_success_reject(self):
        freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":False} 
        response = self.client.post(self.url,valid_request_data)
        self.assertEqual(response.status_code,200)
    def test_respond_friend_request_success_reject_has_database_changed(self):
        freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":False} 
        response = self.client.post(self.url,valid_request_data)

        self.assertEqual(FriendRequestEntry.objects.get(pk=freq.pk).is_accepted,False)
    def test_respond_friend_request_success_correctly_set_data_even_with_invalid_field(self):
        freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":True,'friend':'3'} 
        response = self.client.post(self.url,valid_request_data)
        self.assertEqual(FriendRequestEntry.objects.get(pk=freq.pk).is_accepted,True)
    def test_respond_friend_request_fail_on_invalid_record_id(self):
        invalid_request_data = {"record_id":48949,"is_accepted":True} 
        response = self.client.post(self.url,invalid_request_data)
        self.assertEqual(response.status_code,400)        
    def test_respond_friend_request_fail_on_invalid_data_type(self):
        freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
        invalid_request_data = {"record_id":freq.pk,"is_accepted":"hello"} 
        response = self.client.post(self.url,invalid_request_data)
        self.assertEqual(response.status_code,400)
    def test_respond_friend_request_fail_on_invalid_field(self):
        invalid_request_data = {"record_id":48949} 
        response = self.client.post(self.url,invalid_request_data)
        self.assertEqual(response.status_code,400)        

    def test_respond_friend_request_success_friendship_record_created_me_to_friend(self):
        freq=FriendRequestEntry.objects.create(user=self.friend.user,target=self.user.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
        self.client.post(self.url,valid_request_data)
        record = UnilateralFriendship.objects.get(user=self.user.user,friend=self.friend.user)

        #print(record)
        self.assertIsNotNone(record)
    def test_respond_friend_request_success_friendship_record_created_friend_to_me(self):
        freq=FriendRequestEntry.objects.create(user=self.friend.user,target=self.user.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
        self.client.post(self.url,valid_request_data)
        record = UnilateralFriendship.objects.get(user=self.friend.user,friend=self.user.user)

        #print(record)
        self.assertIsNotNone(record)
    def test_respond_friend_request_success_and_friendship_created_me_to_friend(self):
        freq=FriendRequestEntry.objects.create(user=self.friend.user,target=self.user.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
        self.client.post(self.url,valid_request_data)
        record = UnilateralFriendship.objects.get(user=self.user.user,friend=self.friend.user)

        #print("res:",record)
        self.assertIsNotNone(record)
    def test_respond_friend_request_success_and_friendship_created_friend_to_me(self):
        freq=FriendRequestEntry.objects.create(user=self.friend.user,target=self.user.user)
        valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
        self.client.post(self.url,valid_request_data)
        record = UnilateralFriendship.objects.get(user=self.friend.user,friend=self.user.user)

        #print("res:",record)
        self.assertIsNotNone(record)