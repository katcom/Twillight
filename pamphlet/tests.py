import json
from urllib import response
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from pamphlet.models import FacePamphletUser
from .model_managers import *
from .model_factories import *
# Create your tests here.
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
class StatusTest(APITestCase):
    def setUp(self) -> None:
        mangaer = UserManager()
        self.user = mangaer.create(user_custom_name="Docker",username="8942",password="887788uuy")
        self.url='/api/create-status/'
        self.get_status_url = '/api/get-status/'
        self.client = APIClient()
        self.client.force_login(self.user.user)
        self.status = StatusEntryFactory()
    def test_create_status_success(self):
        valid_post_data={"text_content":"Hello world! 👋","visibility":'PUB'}
        response = self.client.post(self.url,valid_post_data)
        # print(self.user.user.status.all())
        #print("res",response.content)
        self.assertEqual(response.status_code,201)
    def test_get_all_status_success(self):
        url=self.get_status_url+self.status.user.username
        response = self.client.get(url)
        #print(response.content)
        self.assertEqual(response.status_code,200)
    def test_get_status_has_correct_content(self):
        url=self.get_status_url+self.status.user.username
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(data[0]['text_content'],self.status.text_content)