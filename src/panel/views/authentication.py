import random
from datetime import timedelta

from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (login as django_login, logout as django_logout)

from users.models import User
from ..forms import UserLogInForm, UserVerifyForm




def generate_2fa(request):  # NOTE: This is not a view
    request.session["2FA"] = random.randint(1000, 9999)
    request.session["2fa_expire"] = (timezone.now() + timedelta(minutes=1)).strftime("%d/%m/%Y, %H:%M:%S")
    print(f"generated:{request.session['2FA']}  until:{request.session['2fa_expire']}")
    return request




class LoginView(FormView):

    template_name = 'panel/login.html'
    form_class = UserLogInForm
    success_url = reverse_lazy("panel:user_verify")

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, User):
            return redirect("panel:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        phone = str(cd['phone'])
        user = User.objects.filter(phone=phone).first()
        if user:
            self.request.session['user_phone'] = phone
            return super().form_valid(form)
        else:
            form.add_error("phone", "Phone number not found")
            return super().form_invalid(form)



class UserVerifyView(FormView):
    template_name = 'panel/user_verify.html'
    form_class = UserVerifyForm
    success_url = reverse_lazy("panel:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, User):
            return redirect("panel:dashboard")
        self.user_phone = request.session.get('user_phone')
        if not self.user_phone:
            return redirect("panel:login")
        self.generated_otp = request.session.get('2FA')
        self.expiration_time = request.session.get('2fa_expire')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if (not self.expiration_time) or (
            timezone.now() > timezone.datetime.strptime(self.expiration_time, "%d/%m/%Y, %H:%M:%S")
        ):
            request = generate_2fa(request)
        else:
            print(f"previous:{self.generated_otp}  until:{self.expiration_time}")
        return super().get(request)

    def post(self, request):
        if not all([self.generated_otp,self.expiration_time]):
            return redirect("panel:user_verify")
        if timezone.now() > timezone.datetime.strptime(self.expiration_time, "%d/%m/%Y, %H:%M:%S"):
            print("expired")
            self.request = generate_2fa(request)
            form = self.get_form()
            form.add_error("otp", "Previous 2FA code expired. A new code has been sent to you")
            return self.form_invalid(form)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            return self.form_invalid(form)

    def form_valid(self, form):
        entered_otp = form.clean().get('otp')
        if entered_otp == str(self.generated_otp):
            self.request.session.pop('2FA')
            self.request.session.pop('2fa_expire')
            self.request.session["authenticated"] = True
            user = User.objects.get(phone=self.user_phone)
            django_login(self.request, user, "users.auth.UserAuthBackend")
            self.request.session['phone'] = user.phone
            return super().form_valid(form)
        else:
            form.add_error("otp","Invalid code entered")
            return self.form_invalid(form)



@login_required
def logout(request):
    django_logout(request)
    request.session["authenticated"] = False
    request.session["phone"] = None
    request.session["user_phone"] = None
    return redirect("index")
