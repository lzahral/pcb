from django import forms
from .models import Board


class BoardPriceForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['price']

        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'قیمت را وارد کنید'
            })
        }