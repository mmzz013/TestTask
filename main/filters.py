import django_filters
from django_filters import NumberFilter
from geopy.distance import geodesic

from .models import User


class UserFilter(django_filters.FilterSet):
    distance = NumberFilter(method='distance_filter')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'distance']

    def distance_filter(self, queryset, name, value):
        latitude = self.request.user.latitude
        longitude = self.request.user.longitude
        filtered_list = []
        for user in queryset:
            if user.latitude is not None and user.longitude is not None:
                dis = geodesic((latitude, longitude), (user.latitude, user.longitude)).km
                if dis <= value and user.id != self.request.user.id:
                    filtered_list.append(user.id)

        query = User.objects.filter(id__in=filtered_list)
        return query
