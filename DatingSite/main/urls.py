from django.urls import path
from .views import ClientsCreateSet

urlpatterns = [
    path('api/clients/create/', ClientsCreateSet.as_view()),
]
