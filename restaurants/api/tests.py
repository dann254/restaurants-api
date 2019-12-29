import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Restaurant
from .serializers import RestaurantSerializer


# initialize the APIClient app
client = APIClient()

class RestaurantTest(APITestCase):
    """ Test module for Restaurants """

    def setUp(self):
        self.test_restaurant = {'name':'Cool Restaurant'}
        Restaurant.objects.create(
                name=self.test_restaurant['name'])

    def test_get_all_restaurants(self):
        """Test if user can get all restaruants"""
        response = client.get('/restaurants/')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_slug(self):
        """Test if slug is created with  restaurant"""
        restaurant = Restaurant.objects.first()
        self.assertTrue(restaurant.slug)

    def test_get_one_restaurants(self):
        """Test if user can get all restaruants"""
        response = client.get('/restaurants/cool-restaurant/')
        self.assertEqual(response.data['name'], self.test_restaurant['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_restaurants(self):
        """Test if user can search for restaruants"""
        response = client.get('/restaurants/?search=cool')
        self.assertEqual(response.data['results'][0]['name'], self.test_restaurant['name'])
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
