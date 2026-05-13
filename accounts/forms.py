from django.contrib.auth import password_validation
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label=" نام", max_length=150)
    last_name = forms.CharField(label="نام خانوادگی", max_length=150)
    email = forms.EmailField(label="ایمیل")
    password1 = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="تکرار رمز عبور")

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


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='پسورد فعلی')
    new_password = forms.CharField(widget=forms.PasswordInput, label='پسورد جدید')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='تکرار پسورد جدید')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")

        if not self.user.check_password(old_password):
            raise forms.ValidationError("پسورد فعلی اشتباه است")

        return old_password

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("پسورد جدید و تکرار آن برابر نیست")

        return cleaned_data

    def save(self):
        new_password = self.cleaned_data["new_password"]
        self.user.set_password(new_password)
        self.user.save()
        return self.user


class ProfileForm(forms.Form):
    # avatar = forms.ImageField(required=False)
    first_name = forms.CharField(required=False, label='نام')
    last_name = forms.CharField(required=False, label='نام خانوادگی')
    # email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False, label='شماره تلفن')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            profile = self.user.profile

            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["phone_number"].initial = profile.phone_number

    def save(self):
        if not self.user:
            return

        profile = self.user.profile

        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]

        profile.phone_number = self.cleaned_data["phone_number"]

        avatar = self.cleaned_data.get("avatar")
        if avatar:
            profile.avatar = avatar

        self.user.save()
        profile.save()