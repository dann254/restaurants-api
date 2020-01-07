from .models import Restaurant
from datetime import datetime
from rest_framework import viewsets, filters
from rest_framework.response import Response
from restaurants.api.serializers import RestaurantSerializer, RestaurantListSerializer

class ActionBaseSerializerMixin(viewsets.ModelViewSet):
    """
    Pick a serializer based on router action.
    """
    serializer_classes = {
        'default': None,
    }

    def get_serializer_class(self):
        default = self.serializer_classes.get('default')
        serializer_class = self.serializer_classes.get(self.action)
        return serializer_class or default

class StatusFilterMixin(object):
    """
    Filter restaurants based on status.
    """
    def filter_status(self, status):
        result_list = []
        for i in self.queryset:
            if i.open == status :
                result_list.append(i)

        return result_list

    def filter_if_open(self, f_time, weekday):
        result_list = []
        for i in self.queryset:
            current_time = f_time
            schedule = i.schedules.filter(weekday__iso_weekday = weekday).first()
            midnight = datetime.strptime('00:00:00', '%H:%M:%S').time()

            if schedule.opening_time < schedule.closing_time:
                if current_time >= schedule.opening_time and current_time < schedule.closing_time:
                    result_list.append(i)

            elif schedule.add_overflow:
                if current_time >= midnight and current_time <= schedule.add_overflow:
                    result_list.append(i)

            else:
                if current_time >= schedule.opening_time and current_time < midnight:
                    result_list.append(i)


        return result_list


class RestaurantViewSet(ActionBaseSerializerMixin, StatusFilterMixin):
    """
    API endpoint that allows users to view restaruants.
    """
    queryset = Restaurant.objects.all()
    serializer_classes = {
        'default': RestaurantListSerializer,
        'list': RestaurantListSerializer,
        'retrieve': RestaurantSerializer,
    }
    lookup_field = 'slug'
    http_method_names = ['get']

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        """
        This view returns a list of Restaurants
        based on applied filters
        """
        open = self.request.query_params.get('is_open')
        f_time = self.request.query_params.get('time')
        weekday = self.request.query_params.get('weekday')

        if open:
            if open == "True":
                return self.filter_status(True)

            elif open == "False":
                return self.filter_status(False)

        elif f_time and weekday:
            try:
                f_time = datetime.strptime(f_time,'%H:%M:%S').time()
                weekday = int(weekday)
                if not weekday >= 1 and weekday <= 7:
                    weekday = False
            except ValueError:
                f_time = False
                weekday = False

            if weekday and f_time:
                self.queryset = self.queryset.filter(schedules__weekday__iso_weekday=weekday)
                return self.filter_if_open(f_time, weekday)

        elif weekday:
            try:
                weekday = int(weekday)
                if not weekday >= 1 and weekday <= 7:
                    weekday = False
            except ValueError:
                weekday = False


            if weekday:
                return self.queryset.filter(schedules__weekday__iso_weekday=weekday)


        return self.queryset
