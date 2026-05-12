from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import *
from django.views.generic import FormView
from django.urls import reverse_lazy
# Create your views here.


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "accounts/register_form.html"
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        print(form.cleaned_data)
        data = form.cleaned_data

        if data['password1'] != data['password2']:
            form.add_error("password1", "رمز عبورها مطابقت ندارند.")
            return super().form_invalid(form)


        
        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password1']
        )
        profile = form.save()
        profile.user= user
        profile.save()

        return super().form_valid(form)
    

class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/login_form.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.data['login[password]']
        is_error = False
        if username == "":
            is_error = True
            form.add_error("username", "ایمیل خود را وارد کنید.")
        if password == "":
            is_error = True
            form.add_error("password", "رمز عبور خود را وارد کنید.")
        if is_error:
            return super().form_invalid(form)
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(self.request, user)
                # messages.success(self.request,  "Login successful.")

                return super().form_valid(form)
            else:
                form.add_error(
                    "password", "ایمیل یا رمز عبور اشتباه است.")

        return super().form_invalid(form)




