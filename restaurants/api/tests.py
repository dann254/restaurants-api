import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
#from .models import #model
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, GroupSerializer


# initialize the APIClient app
client = APIClient()

class UsersTest(APITestCase):
    """ Test module for GET Users API """

    def setUp(self):
        self.test_user = {'username':'test', 'email':'test@example.com'}
        User.objects.create(
                username=self.test_user['username'], email=self.test_user['email'])

    def test_true_equal_true(self):
        self.assertTrue(True)


    def test_get_all_users(self):
        # get API response
        response = client.get('/users/')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GroupTest(APITestCase):
    """ Test module for GET Groups API """

    def setUp(self):
        self.test_group = {'name':'manager'}
        Group.objects.create(
                name=self.test_group['name'])

    def test_true_equal_true(self):
        self.assertTrue(True)


    def test_get_all_groups(self):
        # get API response
        response = client.get('/groups/')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
