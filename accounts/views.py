from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash, mixins
from django.views.generic import FormView, TemplateView

from .forms import *


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
        login(self.request, user)

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


class ProfileUpdateView(mixins.LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.request.user.profile

        context["profile_form"] = kwargs.get(
            "profile_form",
            ProfileForm(instance=profile,user=self.request.user)
        )

        context["password_form"] = kwargs.get(
            "password_form",
            PasswordChangeForm(user=self.request.user)
        )

        return context

    def post(self, request, *args, **kwargs):

        if "update_profile" in request.POST:
            profile_form = ProfileForm(
                request.POST,
                request.FILES,
                user=request.user
            )

            if profile_form.is_valid():
                profile_form.save()
                return redirect("profile_edit")

            return self.render_to_response(
                self.get_context_data(profile_form=profile_form)
            )

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(
                user=request.user,
                data=request.POST
            )

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "  رمز عبور با موفقیت تغییر کرد.")
                return redirect("profile_edit")

            return self.render_to_response(
                self.get_context_data(password_form=password_form)
            )

        return redirect("profile_edit")




