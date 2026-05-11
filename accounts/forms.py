from django.contrib.auth import password_validation
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label=" نام", max_length=150)
    last_name = forms.CharField(label="نام خانوادگی", max_length=150)
    email = forms.EmailField(label="ایمیل")
    password1 = forms.CharField(widget=forms.PasswordInput, label="پسورد")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="تکرار پسورد")

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'id_code',
                  'commercial_code', 'company', 'postal_code', 'address', 'password1', 'password2']


    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(username=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.user.pk)

        if qs.exists():
            raise forms.ValidationError("کاربری با این ایمیل وجود دارد.")

        return email
    
    
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=False,
        label="ایمیل"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        min_length=4,
        label="رمز عبور"
    )
