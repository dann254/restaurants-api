from .models import Restaurant, Schedule, Weekday
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


class RestaurantSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True, read_only=True)
    open = serializers.ReadOnlyField()
    class Meta:
        model = Restaurant
        fields = ['url', 'name', 'open',  'schedules']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
