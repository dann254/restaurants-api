import json
import csv
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Restaurant
from .serializers import RestaurantSerializer
from django.conf import settings


# initialize the APIClient app
client = APIClient()

class RestaurantTest(APITestCase):
    """ Test module for Restaurants """

    base_url = '/restaurants/'

    def setUp(self):
        self.restaurant_count = 0
        seed_dir = settings.SEED_DIR
        with open(seed_dir + '/restaurants.csv') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader: self.restaurant_count += 1

    def test_get_all_restaurants(self):
        """Test if user can get all restaruants"""
        response = client.get(self.base_url)
        self.assertEqual(response.data['count'], self.restaurant_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_slug(self):
        """Test if slug is created with  restaurant"""
        restaurant = Restaurant.objects.first()
        self.assertTrue(restaurant.slug)

    def test_get_one_restaurants(self):
        """Test if user can get all restaruants"""
        restaurant = client.get(self.base_url)
        slug=restaurant.data['results'][0]['url'].split('/', 4)[4]
        response = client.get(self.base_url + slug)
        self.assertEqual(response.data['name'], restaurant.data['results'][0]['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_restaurants(self):
        """Test if user can search for restaruants"""
        response = client.get(self.base_url + '?search=Restaurant')
        self.assertTrue(response.data['count'] < self.restaurant_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_schedules(self):
        """Test if getting restarant includes schedule"""
        restaurant = client.get(self.base_url)
        slug=restaurant.data['results'][0]['url'].split('/', 4)[4]
        response = client.get(self.base_url + slug)
        self.assertTrue(len(response.data['schedules'])>1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_schedules_weekday(self):
        """Test if restarant schedule includes weekday"""
        restaurant = client.get(self.base_url)
        slug=restaurant.data['results'][0]['url'].split('/', 4)[4]
        response = client.get(self.base_url + slug)
        self.assertTrue(response.data['schedules'][0]['weekday'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
