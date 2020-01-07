from .models import Restaurant, Schedule, Weekday, Review
from rest_framework import serializers

class WeekdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekday
        fields = ['day', 'iso_weekday']


class ScheduleSerializer(serializers.ModelSerializer):
    weekday = WeekdaySerializer(many=False, read_only=True)

    class Meta:
        model = Schedule
        fields = ['opening_time', 'closing_time', 'weekday']

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['rating', 'review', 'created']


class RestaurantSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=False)
    open = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    rating_average = serializers.ReadOnlyField()
    class Meta:
        model = Restaurant
        fields = ['url', 'name', 'open','slug', 'review_count', 'rating_average', 'reviews', 'schedules']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        read_only_fields = ['name', 'open', 'schedules', 'url']

class RestaurantListSerializer(serializers.ModelSerializer):
    open = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    rating_average = serializers.ReadOnlyField()
    class Meta:
        model = Restaurant
        fields = ['url', 'name', 'open', 'slug', 'review_count', 'rating_average']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
