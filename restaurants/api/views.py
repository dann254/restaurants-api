from .models import Restaurant
from rest_framework import viewsets, filters
from restaurants.api.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view restaruants.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    http_method_names = ['get']

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
