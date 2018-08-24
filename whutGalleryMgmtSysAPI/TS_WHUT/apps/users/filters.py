import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = User
        fields = ['if_sign']
