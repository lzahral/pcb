from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Print3D)

@admin.register(Print3DMaterial)
class Print3DMaterialAdmin(admin.ModelAdmin):
    list_display = ('type', 'color', 'is_available', 'display_order')
    list_filter = ('type', 'is_available')
    ordering = ('type', '-is_available', 'display_order', 'id')