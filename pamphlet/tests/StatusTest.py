
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
class StatusTest(APITestCase):
    def setUp(self) -> None:

        self.client.force_login(self.user.user)
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mangaer = UserManager()
        cls.user = mangaer.create(user_custom_name="Docker",username="8942",password="887788uuy")
        cls.url='/api/create-status/'
        cls.get_status_url = '/api/get-status/'
        cls.client = APIClient()

        cls.status = StatusEntryFactory(user=cls.user.user)
    def test_create_status_success(self):
        valid_post_data={"text_content":"Hello world! 👋","visibility":'PUB'}
        response = self.client.post(self.url,valid_post_data)
        # print(self.user.user.status.all())
        #print("res",response.content)
        self.assertEqual(response.status_code,201)
    def test_get_all_status_success(self):
        url=self.get_status_url+self.status.user.username
        print(url)
        response = self.client.get(url)
        #print(response.content)
        self.assertEqual(response.status_code,200)
    def test_get_status_has_correct_content(self):
        url=self.get_status_url+self.status.user.username
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(data[0]['text_content'],self.status.text_content)

class DeleteStatusTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mangaer = UserManager()
        cls.user = mangaer.create(user_custom_name="Docker",username="8942",password="887788uuy")
        cls.friend = mangaer.create(user_custom_name="Friend",username="friend",password="887788uuy")

        cls.url='/api/create-status/'
        cls.delete_status_url = '/api/delete-status/'
        cls.client = APIClient()
        cls.client.force_login(cls.user.user)
        cls.user_status = StatusEntryFactory(user=cls.user.user)
        cls.friend_status = StatusEntryFactory(user=cls.friend.user)

    def setUp(self):
        self.client.force_login(self.user.user)

    def test_delete_status_success(self):
        valid_delete_data={'pk':self.user_status.pk}
        response=self.client.post(self.delete_status_url,valid_delete_data)
        #print(response.content)
        self.assertEqual(response.status_code,200)
    def test_delete_status_failed_on_invalid_user(self):
        invalid_delete_data={'pk':self.friend_status.pk}
        response=self.client.post(self.delete_status_url,invalid_delete_data)
        #print(response.content)
        self.assertEqual(response.status_code,401)
    def test_delete_status_failed_on_invalid_user_2(self):
        self.client.logout();
        self.client.force_login(self.friend.user)
        invalid_delete_data={'pk':self.user_status.pk}
        response=self.client.post(self.delete_status_url,invalid_delete_data)
        #print(response.content)
        self.assertEqual(response.status_code,401)
    def test_delete_status_failed_on_invalid_data(self):
        invalid_delete_data={'user':self.user.pk}
        response=self.client.post(self.delete_status_url,invalid_delete_data)
        print(response.content)
        self.assertEqual(response.status_code,400)
    def test_delete_status_failed_on_empty_data(self):
        invalid_delete_data={}
        response=self.client.post(self.delete_status_url,invalid_delete_data)
        print(response.content)
        self.assertEqual(response.status_code,400)