from django.shortcuts import render, redirect
from .forms import UserLogInForm
from auth import UserAuthBackend
from django import http

def login(request):
    if request.method=="POST":
        form=UserLogInForm(request.POST)
        if form.is_valid():
            cd=form.changed_data
            phone=cd['phone']
            user=UserAuthBackend.authenticate(request, phone)
            if user:
                request.session['user_phone']=phone
                return redirect('verify')
        else:
            return http.HttpResponse('invalid phone number')
    else:
        form=UserLogInForm()
        context={'form':form}
        return render(request, 'Users/login.html', context)