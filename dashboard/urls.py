from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", index, name="index"),
    path("about-us/", views.about_us, name="about_us"),
    path("contact-us/", views.contact_us, name="contact_us"),
    path("technical-guide/", views.technical_guide, name="technical-guide"),
]
