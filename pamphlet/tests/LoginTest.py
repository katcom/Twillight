
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
class LoginTest(APITestCase):
    def setUp(self):
        user_manager = UserManager()
        self.client = APIClient()
        self.url = "/api/login/"
        self.user = user_manager.create(user_custom_name='Json',password='uytnnj992',username='js101')
    def test_login_sucess(self):
        valid_login_data={'user_id':'js101','password':'uytnnj992'}
        response = self.client.post(self.url,valid_login_data)
        self.assertEqual(response.status_code,200)
    def test_login_fail_on_wrong_password(self):
        valid_login_data={'user_id':'js101','password':'123456789'}
        response = self.client.post(self.url,valid_login_data)
        # print(response.content)
        self.assertEqual(response.status_code,400)


class LogoutTest(APITestCase):
    def setUp(self):
        user_manager = UserManager()
        self.client = APIClient()
        self.url = "/api/logout/"
        self.user = user_manager.create(user_custom_name='Json',password='uytnnj992',username='js101')
    def test_logout_sucess(self):
        self.client.force_login(user=self.user.user)
        response = self.client.get(self.url)
        # print(response.content)
        self.assertEqual(response.status_code,200)
    def test_login_fail_on_no_login(self):
        response = self.client.get(self.url)
        # print(response.content)
        self.assertEqual(response.status_code,400)