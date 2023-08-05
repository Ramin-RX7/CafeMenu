
from django.shortcuts import render, redirect
from .forms import UserLogInForm, UserVerifyForm
from django.http import HttpResponse
import random
from users.models import User

def login(request):
    if request.method=="POST":
        form=UserLogInForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            phone=str(cd['phone'])
            user=User.objects.filter(phone=phone).first()
            if user:
                request.session['user_phone']=phone
                return render(request, 'panel/verify.html')
        else:
            return HttpResponse('invalid phone number')
    form=UserLogInForm()
    context={'form':form}
    return render(request, 'panel/login.html', context)
    

def verify(request):
    user_phone = request.session.get('user_phone')
    if user_phone:
        generated_otp = random.randint(1000, 9999)
        request.session['2FA'] = generated_otp
        print(generated_otp)
        form=UserVerifyForm()
        if request.method == 'POST':
            form=UserVerifyForm(request.POST)
            entered_otp = request.POST.get('otp', '')
            generated_otp = request.session.get('2FA')
        if entered_otp == str(generated_otp):
            return redirect('index')  
        else:
            return redirect('verify') 
    return render(request, 'panel/verify.html')

