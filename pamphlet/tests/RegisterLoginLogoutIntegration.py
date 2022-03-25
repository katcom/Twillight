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
class RegisterLoginLogoutIntegration(APITestCase):
    def setUp(self):
        self.login_url ="/api/login/" 
        self.client = APIClient()
        self.register_url = "/api/register/"
        self.logout_url = "/api/logout/"
    def test_register_and_login_success(self):
        valid_register_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
        self.client.post(self.register_url,valid_register_data)
        valid_login_data = {'password':'huyjn9987','user_id':'js101'}
        self.client.post(self.login_url,valid_login_data)
    def test_register_login_logout_success(self):
        valid_register_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
        self.client.post(self.register_url,valid_register_data)
        valid_login_data = {'password':'huyjn9987','user_id':'js101'}
        self.client.post(self.login_url,valid_login_data)
        self.client.post(self.logout_url)