
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


class RegisterTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/register/" 
    def test_register_success(self):
        valid_post_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
        response = self.client.post(self.url,valid_post_data)
        self.assertEqual(response.status_code,201)
    def test_register_success_and_has_user_in_database(self):
        valid_post_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
        response = self.client.post(self.url,valid_post_data)
        user = FacePamphletUser.objects.get(user_custom_name="Json")
        self.assertIsNotNone(user)
    def test_register_fail_on_empty_username(self):
        invalid_post_data = {'username':"",'password':'huyjn9987','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        # print(response.content)
        self.assertEqual(response.status_code,400)
    def test_register_fail_on_empty_user_id(self):
        invalid_post_data = {'username':"Json",'password':'huyjn9987','user_id':''}
        response = self.client.post(self.url,invalid_post_data)
        # print(response.content)
        self.assertEqual(response.status_code,400)
    
    def test_register_fail_on_empty_password(self):
        invalid_post_data = {'username':"Json",'password':'','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        #print(response.content)
        self.assertEqual(response.status_code,400)
    def test_register_fail_on_simple_password_numeric(self):
        invalid_post_data = {'username':"Json",'password':'123456789','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        # print(response.content)
        self.assertEqual(response.status_code,400)
    def test_register_fail_on_simple_password_no_number(self):
        invalid_post_data = {'username':"Json",'password':'abcdefghijk','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        # print(response.content)
        self.assertEqual(response.status_code,400)
    def test_register_fail_on_simple_password_common(self):
        invalid_post_data = {'username':"Json",'password':'1234567a','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        # print(response.content)
        self.assertEqual(response.status_code,400)
    def test_register_fail_on_simple_password_common_2(self):
        invalid_post_data = {'username':"Json",'password':'abcdefg123','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        # print(response.content)
        self.assertEqual(response.status_code,400)
    def test_register_fail_on_user_exist(self):
        valid_post_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
        self.client.post(self.url,valid_post_data)
        response = self.client.post(self.url,valid_post_data)
        #print(response.content)
        self.assertEqual(response.status_code,400)

    def test_register_fail_on_simple_password_digits_only(self):
        invalid_post_data = {'username':"Json",'password':'123456','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        #print(response.content)
        self.assertEqual(response.status_code,400)
    def test_register_fail_on_simple_password_alpha_only(self):
        invalid_post_data = {'username':"Json",'password':'123456','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        #print(response.content)
        self.assertEqual(response.status_code,400)
    def test_register_fail_on_simple_password_too_short(self):
        invalid_post_data = {'username':"Json",'password':'123','user_id':'js101'}
        response = self.client.post(self.url,invalid_post_data)
        #print(response.content)
        self.assertEqual(response.status_code,400)