from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Print3D)
admin.site.register(Print3DMaterial)
