from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from pcb_board.models import hex_to_rgba
from persiantools.jdatetime import JalaliDateTime
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from colorfield.fields import ColorField
from decimal import Decimal


class Order(models.Model):
    STATE_CHOICES = [
        ('pending', 'در حال بررسی'),
        ('pending_payment', 'در انتظار پرداخت'),
        ('pending_receipt', 'در انتظار تایید '),
        ('preparing', 'در پروسه تولید'),
        ('shipping', 'در حال ارسال'),
        ('completed', 'پایان یافته'),
    ]
    DELIVERY_CHOICES = [
        ('post', 'پست معمولی'),
        ('pishtaz', 'پست پیشتاز'),
    ]
    user = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default='pending')
    delivery_type = models.CharField(
        max_length=10, choices=DELIVERY_CHOICES, default='post')
    delivery_price = models.IntegerField(null=True, blank=True)
    tracking_code = models.CharField( max_length=24, null=True, blank=True)

    def total_item_count(self):
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0

    def total_price(self):
        return sum(item.final_price() for item in self.items.all())
    def state_colors(self):
        colors = {
            'pending': "#35b5dc",
            'pending_payment': "#3835dc",
            'preparing': '#fd7e14',
            'shipping': '#ffc107',
            'completed': '#20c997'
        }

        hex_color = colors.get(self.state, '#6c757d')

        return {
            "text": hex_color,
            "bg": hex_to_rgba(hex_color, 0.1)
        }
    def get_date(self):
        months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد',
                  'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        date = self.created_at
       
        date = JalaliDate(date)
        date = f"{date.day} {months[date.month-1]} {date.year}"
        return date


    def __str__(self):
        return f'Order {self.id} by {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(null=True, blank=True)

    def total_price(self):
        return self.quantity * self.product.price or 0

    def final_price(self):
        return self.quantity * self.price or 0

    def __str__(self):
        return f'{self.quantity} x {self.product.name} {self.id}'

class Print3DMaterial (models.Model):
    TYPE_CHOICES = [
        ('ABS', 'ABS'),
        ('PLA', 'PLA'),
        ('PETG', 'PETG'),
    ]
    type = models.CharField(
        max_length=5, choices=TYPE_CHOICES, default='ABS', verbose_name='متریال')
    color = models.CharField(max_length=12, verbose_name='رنگ')
    is_available = models.BooleanField(default=True)
    color_hex = ColorField(default='#FF0000', verbose_name='رنگ')
    display_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    price_per_kg = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='قیمت هر کیلوگرم'
    )



    @property
    def price_per_gram(self):
        return self.price_per_kg / Decimal('1000')
    

    def __str__(self):
        return f' {self.display_order} - {self.type} - {self.color}'
    class Meta:
        verbose_name = 'متریال چاپ سه‌بعدی'
        verbose_name_plural = 'متریال‌های چاپ سه‌بعدی'
        ordering = ['-is_available', '-display_order', 'id']

class Print3D(models.Model):
    TYPE_CHOICES = [
        ('ABS', 'ABS'),
        ('PLA', 'PLA'),
        ('PETG', 'PETG'),
    ]
    INFILL_CHOICES = [
        ('10', '10'),
        ('20', '20'),
        ('30', '30'),
        ('40', '40'),
        ('50', '50'),
        ('60', '60'),
        ('70', '70'),
        ('80', '80'),
        ('90', '90'),
        ('100', '100'),
    ]
    STATE_CHOICES = [
        ('pending', 'در حال بررسی'),
        ('pending_payment', 'در انتظار پرداخت'),
        ('pending_receipt', 'در انتظار تایید '),
        ('preparing', 'در پروسه تولید'),
        ('shipping', 'در حال ارسال'),
        ('completed', 'پایان یافته'),
    ]
    order = models.ForeignKey(
        Order, related_name='print3d', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        Profile, related_name='print3d', on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to="uploads/print3D/", verbose_name="فایل")
    
    infill = models.CharField(  max_length=3, choices=INFILL_CHOICES,default='10', verbose_name='تراکم', null=True, blank=True)
    material = models.ForeignKey(
        Print3DMaterial, related_name='print3d', on_delete=models.CASCADE, null=True, blank=True)
    # material = models.CharField(
    #     max_length=5, choices=TYPE_CHOICES, default='ABS', verbose_name='متریال',null=True, blank=True)
    # color = models.CharField(max_length=12, verbose_name='رنگ',null=True, blank=True)

    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default='pending')
    image = models.ImageField(upload_to='stl_images/', null=True, blank=True)
    qty = models.IntegerField(verbose_name='تعداد')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)
    payment_receipt = models.FileField(upload_to='uploads/receipts/', null=True, blank=True)

    class Meta:
        verbose_name = "print3D"
        verbose_name_plural = "print3Ds"

    def __str__(self):
        return f'{self.material} {self.qty}'
    def price_unit(self):
        return self.price/int(self.qty)
        

    def get_date(self):
        return convert_date_to_jalali(self.created_at)
    def state_colors(self):
        colors = {
            'pending': "#35b5dc",
            'pending_payment': "#3835dc",
            'preparing': '#fd7e14',
            'shipping': '#ffc107',
            'completed': '#20c997'
        }

        hex_color = colors.get(self.state, '#6c757d')

        return {
            "text": hex_color,
            "bg": hex_to_rgba(hex_color, 0.1)
        }

def convert_date_to_jalali(item):
    date = '-'
    if item:
        date = JalaliDateTime(
            item + timedelta(hours=3, minutes=30)).strftime("%Y/%m/%d %H:%M:%S")
    return date
