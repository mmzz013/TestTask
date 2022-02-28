from django.urls import path
from .views import index
from .views import ClientsCreateSet, UserView
from rest_framework import routers


urlpatterns = [
    path('', index),
    path('api/clients/create/', ClientsCreateSet.as_view()),
    path('api/list/', UserView.as_view()),

]
