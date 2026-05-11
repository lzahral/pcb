from django.urls import path
from .views import *

urlpatterns = [
    path("", PCBCreateView.as_view(), name="index_2"),
]
