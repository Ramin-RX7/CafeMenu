import json
import random
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (login as django_login, logout as django_logout)
from django.core.cache import caches

from users.models import User, Client
from ..forms import UserLogInForm



AUTH_CACHE = caches["default"]



def generate_2fa():
    return "".join(random.choices("0123456789", k=6))



class LoginView(FormView):

    template_name = 'panel/login.html'
    form_class = UserLogInForm
    client_success_url = reverse_lazy("foods:menu")
    staff_success_url = reverse_lazy("panel:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, User):
            return redirect("panel:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print(list(request.POST.items()))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        phone = str(cd['phone'])
        code = str(cd["otp_code"])
        cache_code = AUTH_CACHE.get(phone)
        if cache_code != code:
            form.add_error("otp_code", "Invalid code")
            return super().form_invalid(form)
        user = User.objects.filter(phone=phone).first()
        if not user:  # User is not staff, hence we create a Client (unusable password)
            user = Client.objects.create(phone=phone)
        django_login(self.request, user, "users.auth.UserAuthBackend")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        if self.request.user.is_staff:
            return self.staff_success_url
        return self.client_success_url


class SendOTPView(View):
    def post(self, request):
        data = json.loads(request.body)
        phone = data.get("phone")
        AUTH_CACHE.set(phone, generate_2fa())
        return JsonResponse({"result":"ok"})


@login_required
def logout(request):
    django_logout(request)
    return redirect("index")
