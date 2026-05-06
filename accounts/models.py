from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'staff'),
        ('customer', 'Customer'),
    )

    phone_number = models.CharField(max_length=11, null=True, blank=True,verbose_name='شماره همراه')

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='profile'
    )

    id_code = models.CharField(max_length=11, verbose_name='کدملی / شناسه‌ملی')
    company = models.CharField(max_length=11, verbose_name='شرکت')
    postal_code = models.CharField(max_length=11, verbose_name='کدپستی')
    commercial_code = models.CharField(max_length=11, verbose_name='کداقتصادی')
    address = models.TextField( verbose_name='آدرس')

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )


