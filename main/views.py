from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import UserFilter
from .models import User
from .serializers import UserSerializer
from .services import handle_match_request


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


class MatchView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def match(self, request, *args, **kwargs):
        client_id = kwargs.get("client_id")
        if client_id == request.user.id:
            return Response(data={"error": "Нельзя отправлять запрос самому себе"}, status=400)

        liked_person_email = handle_match_request(request.user, kwargs.get("client_id"))

        if liked_person_email:
            data = {
                "matched": True,
                "email": liked_person_email
            }
        else:
            data = {
                "matched": False,
            }
        return Response(data=data, status=200)
