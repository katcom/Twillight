import json
import os
from pydoc import resolve
from urllib import request, response
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from pamphlet.models import FacePamphletUser
from .model_managers import *
from .model_factories import *
from datetime import *
import time
import shutil
# Create your tests here.
# class RegisterTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = "/api/register/" 
#     def test_register_success(self):
#         valid_post_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
#         response = self.client.post(self.url,valid_post_data)
#         self.assertEqual(response.status_code,201)
#     def test_register_success_and_has_user_in_database(self):
#         valid_post_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
#         response = self.client.post(self.url,valid_post_data)
#         user = FacePamphletUser.objects.get(user_custom_name="Json")
#         self.assertIsNotNone(user)
#     def test_register_fail_on_empty_username(self):
#         invalid_post_data = {'username':"",'password':'huyjn9987','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         # print(response.content)
#         self.assertEqual(response.status_code,400)
#     def test_register_fail_on_empty_user_id(self):
#         invalid_post_data = {'username':"Json",'password':'huyjn9987','user_id':''}
#         response = self.client.post(self.url,invalid_post_data)
#         # print(response.content)
#         self.assertEqual(response.status_code,400)
    
#     def test_register_fail_on_empty_password(self):
#         invalid_post_data = {'username':"Json",'password':'','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         #print(response.content)
#         self.assertEqual(response.status_code,400)
#     def test_register_fail_on_simple_password_numeric(self):
#         invalid_post_data = {'username':"Json",'password':'123456789','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         # print(response.content)
#         self.assertEqual(response.status_code,400)
#     def test_register_fail_on_simple_password_no_number(self):
#         invalid_post_data = {'username':"Json",'password':'abcdefghijk','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         # print(response.content)
#         self.assertEqual(response.status_code,400)
#     def test_register_fail_on_simple_password_common(self):
#         invalid_post_data = {'username':"Json",'password':'1234567a','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         # print(response.content)
#         self.assertEqual(response.status_code,400)
#     def test_register_fail_on_simple_password_common_2(self):
#         invalid_post_data = {'username':"Json",'password':'abcdefg123','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         # print(response.content)
#         self.assertEqual(response.status_code,400)
#     def test_register_fail_on_user_exist(self):
#         valid_post_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
#         self.client.post(self.url,valid_post_data)
#         response = self.client.post(self.url,valid_post_data)
#         #print(response.content)
#         self.assertEqual(response.status_code,400)

#     def test_register_fail_on_simple_password_digits_only(self):
#         invalid_post_data = {'username':"Json",'password':'123456','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         #print(response.content)
#         self.assertEqual(response.status_code,400)
#     def test_register_fail_on_simple_password_alpha_only(self):
#         invalid_post_data = {'username':"Json",'password':'123456','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         #print(response.content)
#         self.assertEqual(response.status_code,400)
#     def test_register_fail_on_simple_password_too_short(self):
#         invalid_post_data = {'username':"Json",'password':'123','user_id':'js101'}
#         response = self.client.post(self.url,invalid_post_data)
#         #print(response.content)
#         self.assertEqual(response.status_code,400)

# class LoginTest(APITestCase):
#     def setUp(self):
#         user_manager = UserManager()
#         self.client = APIClient()
#         self.url = "/api/login/"
#         self.user = user_manager.create(user_custom_name='Json',password='uytnnj992',username='js101')
#     def test_login_sucess(self):
#         valid_login_data={'user_id':'js101','password':'uytnnj992'}
#         response = self.client.post(self.url,valid_login_data)
#         self.assertEqual(response.status_code,200)
#     def test_login_fail_on_wrong_password(self):
#         valid_login_data={'user_id':'js101','password':'123456789'}
#         response = self.client.post(self.url,valid_login_data)
#         # print(response.content)
#         self.assertEqual(response.status_code,400)

# class LogoutTest(APITestCase):
#     def setUp(self):
#         user_manager = UserManager()
#         self.client = APIClient()
#         self.url = "/api/logout/"
#         self.user = user_manager.create(user_custom_name='Json',password='uytnnj992',username='js101')
#     def test_logout_sucess(self):
#         self.client.force_login(user=self.user.user)
#         response = self.client.get(self.url)
#         # print(response.content)
#         self.assertEqual(response.status_code,200)
#     def test_login_fail_on_no_login(self):
#         response = self.client.get(self.url)
#         # print(response.content)
#         self.assertEqual(response.status_code,400)
# class StatusTest(APITestCase):
#     def setUp(self) -> None:
#         mangaer = UserManager()
#         self.user = mangaer.create(user_custom_name="Docker",username="8942",password="887788uuy")
#         self.url='/api/create-status/'
#         self.get_status_url = '/api/get-status/'
#         self.client = APIClient()
#         self.client.force_login(self.user.user)
#         self.status = StatusEntryFactory()
#     def test_create_status_success(self):
#         valid_post_data={"text_content":"Hello world! 👋","visibility":'PUB'}
#         response = self.client.post(self.url,valid_post_data)
#         # print(self.user.user.status.all())
#         #print("res",response.content)
#         self.assertEqual(response.status_code,201)
#     def test_get_all_status_success(self):
#         url=self.get_status_url+self.status.user.username
#         response = self.client.get(url)
#         #print(response.content)
#         self.assertEqual(response.status_code,200)
#     def test_get_status_has_correct_content(self):
#         url=self.get_status_url+self.status.user.username
#         response = self.client.get(url)
#         data = json.loads(response.content)
#         self.assertEqual(data[0]['text_content'],self.status.text_content)

# class FriendRequestTest(APITestCase):
#     def setUp(self) -> None:
#         mangaer = UserManager()
#         self.user = mangaer.create(user_custom_name="user",username="user",password="887788uuy")
#         self.friend = mangaer.create(user_custom_name="friend",username="friend",password="885485tghq")
#         self.url='/api/make-friend-request/'
#         self.client = APIClient()
#         self.client.force_login(self.user.user)
#         self.url_respond_request='/api/respond-friend-request/'
#     def test_create_friend_request_success(self):
#         valid_request_data = {"target_id":"friend"} 
#         response = self.client.post(self.url,valid_request_data)
#         #print(response.content)
#         self.assertEqual(response.status_code,201)
#     # def test_create_friend_request_failed_on_invalid_user_id(self):
#     #     valid_request_data = {"user_id":"xxxxx","target_id":"friend"} 
#     #     response = self.client.post(self.url,valid_request_data)
#     #     #print(response.content)
#     #     self.assertEqual(response.status_code,400)
#     def test_create_friend_request_failed_on_invalid_target_id(self):
#         valid_request_data = {"target_id":"xxxxxx"} 
#         response = self.client.post(self.url,valid_request_data)
#         #print(response.content)
#         self.assertEqual(response.status_code,400)

# class FriendRequestRespondTest(APITestCase):
#     def setUp(self) -> None:
#         mangaer = UserManager()
#         self.user = mangaer.create(user_custom_name="user",username="user",password="887788uuy")
#         self.friend = mangaer.create(user_custom_name="friend",username="friend",password="885485tghq")
#         #self.friend = mangaer.create(user_custom_name="third_guy",username="third_guy",password="885485tghq")

#         self.client = APIClient()
#         self.client.force_login(self.user.user)
#         self.url='/api/respond-friend-request/'
#     def test_respond_friend_request_success(self):
#         freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
#         response = self.client.post(self.url,valid_request_data)
#         self.assertEqual(response.status_code,200)
#     def test_respond_friend_request_success_accept_has_database_changed(self):
#         freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
#         response = self.client.post(self.url,valid_request_data)
#         self.assertEqual(FriendRequestEntry.objects.get(pk=freq.pk).is_accepted,True)
#     def test_respond_friend_request_success_reject(self):
#         freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":False} 
#         response = self.client.post(self.url,valid_request_data)
#         self.assertEqual(response.status_code,200)
#     def test_respond_friend_request_success_reject_has_database_changed(self):
#         freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":False} 
#         response = self.client.post(self.url,valid_request_data)

#         self.assertEqual(FriendRequestEntry.objects.get(pk=freq.pk).is_accepted,False)
#     def test_respond_friend_request_success_correctly_set_data_even_with_invalid_field(self):
#         freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":True,'friend':'3'} 
#         response = self.client.post(self.url,valid_request_data)
#         self.assertEqual(FriendRequestEntry.objects.get(pk=freq.pk).is_accepted,True)
#     def test_respond_friend_request_fail_on_invalid_record_id(self):
#         invalid_request_data = {"record_id":48949,"is_accepted":True} 
#         response = self.client.post(self.url,invalid_request_data)
#         self.assertEqual(response.status_code,400)        
#     def test_respond_friend_request_fail_on_invalid_data_type(self):
#         freq=FriendRequestEntry.objects.create(user=self.user.user,target=self.friend.user)
#         invalid_request_data = {"record_id":freq.pk,"is_accepted":"hello"} 
#         response = self.client.post(self.url,invalid_request_data)
#         self.assertEqual(response.status_code,400)
#     def test_respond_friend_request_fail_on_invalid_field(self):
#         invalid_request_data = {"record_id":48949} 
#         response = self.client.post(self.url,invalid_request_data)
#         self.assertEqual(response.status_code,400)        

#     def test_respond_friend_request_success_friendship_record_created_me_to_friend(self):
#         freq=FriendRequestEntry.objects.create(user=self.friend.user,target=self.user.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
#         self.client.post(self.url,valid_request_data)
#         record = ValidUnilateralFriendship.objects.get(friendship__user=self.user.user,friendship__friend=self.friend.user)

#         #print(record)
#         self.assertIsNotNone(record)
#     def test_respond_friend_request_success_friendship_record_created_friend_to_me(self):
#         freq=FriendRequestEntry.objects.create(user=self.friend.user,target=self.user.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
#         self.client.post(self.url,valid_request_data)
#         record = ValidUnilateralFriendship.objects.get(friendship__user=self.friend.user,friendship__friend=self.user.user)

#         #print(record)
#         self.assertIsNotNone(record)
#     def test_respond_friend_request_success_and_friendship_created_me_to_friend(self):
#         freq=FriendRequestEntry.objects.create(user=self.friend.user,target=self.user.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
#         self.client.post(self.url,valid_request_data)
#         record = UnilateralFriendship.objects.get(user=self.user.user,friend=self.friend.user)

#         #print("res:",record)
#         self.assertIsNotNone(record)
#     def test_respond_friend_request_success_and_friendship_created_friend_to_me(self):
#         freq=FriendRequestEntry.objects.create(user=self.friend.user,target=self.user.user)
#         valid_request_data = {"record_id":freq.pk,"is_accepted":True} 
#         self.client.post(self.url,valid_request_data)
#         record = UnilateralFriendship.objects.get(user=self.friend.user,friend=self.user.user)

#         #print("res:",record)
#         self.assertIsNotNone(record)

# class RegisterLoginLogoutIntegration(APITestCase):
#     def setUp(self):
#         self.login_url ="/api/login/" 
#         self.client = APIClient()
#         self.register_url = "/api/register/"
#         self.logout_url = "/api/logout/"
#     def test_register_and_login_success(self):
#         valid_register_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
#         self.client.post(self.register_url,valid_register_data)
#         valid_login_data = {'password':'huyjn9987','user_id':'js101'}
#         self.client.post(self.login_url,valid_login_data)
#     def test_register_login_logout_success(self):
#         valid_register_data = {'username':"Json",'password':'huyjn9987','user_id':'js101'}
#         self.client.post(self.register_url,valid_register_data)
#         valid_login_data = {'password':'huyjn9987','user_id':'js101'}
#         self.client.post(self.login_url,valid_login_data)
#         self.client.post(self.logout_url)

# class MakeAndAcceptFriendRequestIntegration(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         mangaer = UserManager()

#         cls.user = mangaer.create(user_custom_name="user",username="user",password="887788uuy")
#         cls.friend = mangaer.create(user_custom_name="friend",username="friend",password="885485tghq")
#         cls.accept_request_url='/api/respond-friend-request/'
#         cls.make_request_url='/api/make-friend-request/'
#     def setUp(self):
#         self.client = APIClient()
#     def test_make_and_accept_friend_request_success(self):
#         self.client.force_login(self.user.user)
#         valid_request_data = {"target_id":"friend"} 
#         self.client.post(self.make_request_url,valid_request_data)
#         self.client.logout()
#         self.client.force_login(self.friend.user)
#         valid_accept_data = {"record_id":"1","is_accepted":"True"} 
#         self.client.post(self.accept_request_url,valid_accept_data)
#         friend_record = ValidUnilateralFriendship.objects.get(friendship__user=self.user.user,friendship__friend=self.friend.user)
#         #print(friend_record) 
#         self.assertIsNotNone(friend_record)
#         friend_record = ValidUnilateralFriendship.objects.get(friendship__user=self.friend.user,friendship__friend=self.user.user)
#         #print(friend_record) 
#         self.assertIsNotNone(friend_record)
#     def test_make_and_reject_friend_request_success(self):
#         self.client.force_login(self.user.user)
#         valid_request_data = {"target_id":"friend"} 
#         self.client.post(self.make_request_url,valid_request_data)
#         self.client.logout()
#         self.client.force_login(self.friend.user)
#         valid_accept_data = {"record_id":"1","is_accepted":"False"} 
#         self.client.post(self.accept_request_url,valid_accept_data)
#         has_user = ValidUnilateralFriendship.objects.filter(friendship__user=self.user.user,friendship__friend=self.friend.user).exists()
#         #print(friend_record) 
#         self.assertFalse(has_user)
#         has_friend = ValidUnilateralFriendship.objects.filter(friendship__user=self.friend.user,friendship__friend=self.user.user).exists()
#         #print(friend_record) 
#         self.assertFalse(has_friend)

# class PrivateChatRoomManagerTest(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         user_manager = UserManager()
#         cls.room_manager = PrivateChatRoomManager()

#         cls.user = user_manager.create(user_custom_name="user",username="user",password="887788uuy")
#         cls.friend = user_manager.create(user_custom_name="friend",username="friend",password="885485tghq")
#         cls.room = PrivateChatRoom.objects.create(user_1 = cls.user.user,user_2=cls.friend.user)
#         cls.accept_request_url='/api/respond-friend-request/'
#         cls.make_request_url='/api/make-friend-request/'
#     def setUp(self):
#         self.client = APIClient()
#     def test_room_manager_get_room_name_success(self):
#         room_name = self.room_manager.get_or_create(self.user.user.username,self.friend.user.username)
#         self.assertEqual(room_name.room_id,self.room.room_id)
#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
# class FriendStatusTest(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user_manager = UserManager()

#         cls.friendship_manager = FriendshipManager()
#         cls.user = cls.user_manager.create(user_custom_name="user",username="unittest_user",password="887788uuy")
#         cls.friend_1 = cls.user_manager.create(user_custom_name="friend",username="unittest_friend",password="885485tghq")
#         cls.friend_2 = cls.user_manager.create(user_custom_name="friend",username="unittest_friend_2",password="885485tghq")
#         cls.stranger = cls.user_manager.create(user_custom_name="friend",username="unittest_stranger",password="885485tghq")
#         cls.status_user_1_pub = StatusEntryFactory(user=cls.user.user,visibility=Visibility.PUBLIC_VIEW)
#         cls.status_friend_1_PUB = StatusEntryFactory(user=cls.friend_1.user,visibility=Visibility.PUBLIC_VIEW)
#         cls.status_friend_1_FRI = StatusEntryFactory(user=cls.friend_2.user,visibility=Visibility.FRIENDS_ONLY_VIEW)
#         cls.status_friend_1_PRI = StatusEntryFactory(user=cls.friend_2.user,visibility=Visibility.PRIVATE_VIEW)
#         cls.status_friend_2_pub = StatusEntryFactory(user=cls.friend_2.user,visibility=Visibility.PUBLIC_VIEW)
#         cls.status_stranger_pub = StatusEntryFactory(user=cls.stranger.user,visibility=Visibility.PUBLIC_VIEW)

#         cls.status_image = StatusImageFactory(status_entry=cls.status_friend_1_FRI)
#         cls.friendship_manager.create(cls.user.user,cls.friend_1.user)
#         cls.friendship_manager.create(cls.user.user,cls.friend_2.user)
#     def setUp(self):
#         self.client = APIClient()
#         self.url='/api/get-friends-status/'
#         self.client.force_login(self.user.user)
#     def test_get_friend_status_success(self):
#         print(self.url)
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code,200)
#     def test_has_all_status_got(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         print(data)
#         self.assertEqual(len(data),3)
#     def test_user_id_is_returned(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         self.assertIn(data[0]['user_id'],[self.friend_1.user.username,self.friend_2.user.username])
#     def test_user_custom_name_is_returned(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         self.assertIn(data[0]['user_custom_name'],[self.friend_1.user_custom_name,self.friend_2.user_custom_name])
#     def test_user_text_content_is_returned(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         self.assertIn(data[0]['text_content'],[self.status_friend_1_PUB.text_content,self.status_friend_1_FRI.text_content,self.status_friend_2_pub.text_content])
#     def test_user_visibility_is_returned(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         self.assertIn(data[0]['visibility'],['PRI','FRI','PUB'])
#     def test_creation_date_is_returned(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         self.assertIsNotNone(data[0]['creation_date'])
#     def test_last_edited_is_returned(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         self.assertIsNotNone(data[0]['last_edited'])
#     def test_private_status_is_not_returned(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         self.assertNotIn(self.status_friend_1_PRI.pk,[e['pk'] for e in data])
#     def test_strangers_status_is_not_returned(self):
#         response = self.client.get(self.url)
#         data = json.loads(response.content)
#         self.assertNotIn(self.status_stranger_pub.pk,[e['pk'] for e in data])
#     def test_image_is_returned(self):
#         pass
#     @classmethod
#     def tearDownClass(cls):
#         directory='UserAppData//'
#         for filename in os.listdir(directory):
#             f = os.path.join(directory, filename)
#             if filename.startswith('unittest') and os.path.isdir(f):
#                 # checking if it is a file
#                 print('remove test data:',f)
#                 shutil.rmtree(f)
#         super().tearDownClass()

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