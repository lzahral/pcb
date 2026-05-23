# forms.py
from django import forms
from .models import Print3D


class STLUploadForm(forms.ModelForm):
    class Meta:
        model = Print3D
        fields = ['file']


class PrintPriceForm(forms.ModelForm):
    class Meta:
        model =Print3D
        fields = ['price']

        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'قیمت را وارد کنید'
            })
        }
class PaymentReceiptForm(forms.ModelForm):
    class Meta:
        model = Print3D
        fields = ['payment_receipt']