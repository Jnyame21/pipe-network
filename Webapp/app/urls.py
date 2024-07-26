from django.urls import path 
from .views import *



urlpatterns = [
    path('', root),
    path('pipe-network', pipe_network_view),
]


