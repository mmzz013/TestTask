from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .filters import UserFilter
from .models import User
from .serializers import UserSerializer


def index(request):
    return HttpResponse('Hello!')


class ClientsCreateSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['first_name', 'last_name', 'gender', 'distance']
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
