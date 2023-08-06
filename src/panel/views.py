import random
from datetime import timedelta

from django.shortcuts import render, redirect
from django.utils import timezone

from users.models import User
from .forms import UserLogInForm, UserVerifyForm



def login(request):
    form=UserLogInForm()
    if request.method=="POST":
        form=UserLogInForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            phone=str(cd['phone'])
            user=User.objects.filter(phone=phone).first()
            if user:
                request.session['user_phone']=phone
                return redirect("panel:user_verify")
            else:
                form.add_error("phone", "Phone number not found")
        else:
            # form.add_error("phone", "Invalid phone number")
            pass
    context={'form':form}
    return render(request, 'panel/login.html', context)


def generate_2fa(request):
    request.session["2FA"] = random.randint(1000, 9999)
    request.session["2fa_expire"] = (timezone.now() + timedelta(minutes=1)).strftime("%d/%m/%Y, %H:%M:%S")
    print(f"generated:{request.session['2FA']}  until:{request.session['2fa_expire']}")
    return request


def user_verify(request):
    user_phone = request.session.get('user_phone')
    if not user_phone:
        return redirect("panel:login")
    generated_otp = request.session.get('2FA')
    expiration_time = request.session.get('2fa_expire')

    if request.method == "GET":
        form = UserVerifyForm()
        if (not expiration_time) or (
            timezone.now() > timezone.datetime.strptime(expiration_time, "%d/%m/%Y, %H:%M:%S")
        ):
            request = generate_2fa(request)
        else:
            # form.add_error("already generated")
            print(f"previous:{generated_otp}  until:{expiration_time}")
        return render(request, 'panel/user_verify.html', {'form': form})

    elif request.method == "POST":
        form = UserVerifyForm(request.POST)
        if timezone.now() > timezone.datetime.strptime(expiration_time, "%d/%m/%Y, %H:%M:%S"):
            print("expired")
            request = generate_2fa(request)
            form.add_error(None, "Previous 2FA code expired. A new code has been sent to you")
            return render(request, 'panel/user_verify.html', {'form': form})
        else:
            if form.is_valid():
                entered_otp = form.cleaned_data.get('otp')
                if entered_otp == str(generated_otp):
                    request.session.pop('2FA')
                    request.session.pop('2fa_expire')
                    request.session["authenticated"] = True
                    return redirect("index")
                else:
                    form.add_error(None,"Invalid code entered")
                    return render(request, 'panel/user_verify.html', {'form': form})
            else:
                ...
