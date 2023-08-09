import random
from typing import Any
from datetime import timedelta

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from users.models import User
from orders.models import Order, Table, OrderItem
from .forms import UserLogInForm, UserVerifyForm
from .urls import *
from .forms import EditOrderForm, EditOrderItemForm



# Create your views here.


def login(request):
    if isinstance(request.user, User):
        return redirect("index")
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
    if isinstance(request.user, User):
        return redirect("index")
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
                    user = User.objects.get(phone=user_phone)
                    django_login(request, user, "users.auth.UserAuthBackend")
                    request.session['phone'] = user.phone
                    return redirect("index")
                else:
                    form.add_error(None,"Invalid code entered")
                    return render(request, 'panel/user_verify.html', {'form': form})
            else:
                ...



def dashboard_staff(request):
    orders = Order.objects.order_by('status')
    tables = Table.objects.all()
    context = {
        'orders': orders,
        'tables': tables,
    }
    return render(request,'panel/dashboard_staff.html', context)


class EditOrders(View):
    def dispatch(self, request, order_id:int):
        self.order = get_object_or_404(Order, id=order_id)
        self.order_items = self.order.orderitem_set.all()
        return super().dispatch(request, order_id)

    def get(self, request, order_id:int):
        form =EditOrderForm(instance=self.order)
        item_forms = []
        for i in self.order_items:
            item_forms.append(EditOrderItemForm(instance=i, initial={"id":i.id}))

        context = {'form':form,'order':self.order, 'orderitems':item_forms}

        return render(request,'panel/dashboard_editoreder.html',context)

    def post(self, request, order_id):
        if request.POST.get("order"):
            form = EditOrderForm(request.POST, instance=self.order)
            if form.is_valid():
                form.save()
                return redirect("panel:dashboard")
            else:
                form.add_error(None,"Invalid input")
        elif request.POST.get("orderitem"):
            item = OrderItem.objects.get(id=request.POST["id"])
            if request.POST["orderitem"] == "delete":
                item.delete()
            else:
                itemform = EditOrderItemForm(request.POST, instance=item)
                if itemform.is_valid():
                    cd=itemform.cleaned_data
                    item.quantity = cd["quantity"]
                    item.food = cd["food"]
                    item.save()
                else:
                    itemform.add_error(None,"Invalid input")
        return redirect("panel:edit_order",order_id=order_id)



def simple_action(view_func):
    def _wrapped_view(request, order_id, *args, **kwargs):
        response = view_func(request, order_id, *args, **kwargs)
        return redirect("panel:dashboard")
    return _wrapped_view

@simple_action
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.approve()

@simple_action
def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.reject()

@simple_action
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.pay()

@simple_action
def deliver_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.deliver()