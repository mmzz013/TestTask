from django.urls import path
from .views import index, MatchView
from .views import ClientsCreateSet, UserView


urlpatterns = [
    path('', index),
    path('api/clients/create/', ClientsCreateSet.as_view()),
    path('api/list/', UserView.as_view()),
    path('api/clients/<int:client_id>/match/', MatchView.as_view({'post': 'match'})),
]
