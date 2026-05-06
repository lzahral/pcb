from django.shortcuts import render
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
            form.add_error("password1", "پسوردها مطابقت ندارند.")
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
