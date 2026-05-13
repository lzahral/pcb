from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'staff'),
        ('customer', 'Customer'),
    )

    phone_number = models.CharField(max_length=11,verbose_name='شماره همراه')

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,blank=True,
        related_name='profile'
    )

    id_code = models.CharField(max_length=11, verbose_name='کدملی / شناسه‌ملی', null=True, blank=True)
    company = models.CharField(max_length=11, verbose_name='شرکت', null=True, blank=True)
    postal_code = models.CharField(max_length=11, verbose_name='کدپستی')
    commercial_code = models.CharField(max_length=11, verbose_name='کداقتصادی', null=True, blank=True)
    address = models.TextField( verbose_name='آدرس')

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    def __str__(self):
        return f'{self.user.get_full_name()}' if self.user else '-'
    
