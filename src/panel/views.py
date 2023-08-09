import random
from datetime import timedelta

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import (login as django_login, logout as django_logout)
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Case, CharField, Value, When

from users.models import User
from orders.models import Order, Table, OrderItem
from foods.models import Food
from .forms import UserLogInForm, UserVerifyForm
from .urls import *
from .forms import EditOrderForm, EditOrderItemForm, AddOrderItemForm



# Create your views here.


class LoginView(View):

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, User):
            return redirect("panel:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
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

    def get(self, request):
        form=UserLogInForm()
        context={'form':form}
        return render(request, 'panel/login.html', context)


def generate_2fa(request):
    request.session["2FA"] = random.randint(1000, 9999)
    request.session["2fa_expire"] = (timezone.now() + timedelta(minutes=1)).strftime("%d/%m/%Y, %H:%M:%S")
    print(f"generated:{request.session['2FA']}  until:{request.session['2fa_expire']}")
    return request



class UserVerifyView(View):
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
        form = UserVerifyForm()
        if (not self.expiration_time) or (
            timezone.now() > timezone.datetime.strptime(self.expiration_time, "%d/%m/%Y, %H:%M:%S")
        ):
            request = generate_2fa(request)
        else:
            # form.add_error("already generated")
            print(f"previous:{self.generated_otp}  until:{self.expiration_time}")
        return render(request, 'panel/user_verify.html', {'form': form})

    def post(self, request):
        if not all([self.generated_otp,self.expiration_time]):
            return redirect("panel:user_verify")
        form = UserVerifyForm(request.POST)
        if timezone.now() > timezone.datetime.strptime(self.expiration_time, "%d/%m/%Y, %H:%M:%S"):
            print("expired")
            request = generate_2fa(request)
            form.add_error(None, "Previous 2FA code expired. A new code has been sent to you")
            return render(request, 'panel/user_verify.html', {'form': form})
        else:
            if form.is_valid():
                entered_otp = form.cleaned_data.get('otp')
                if entered_otp == str(self.generated_otp):
                    request.session.pop('2FA')
                    request.session.pop('2fa_expire')
                    request.session["authenticated"] = True
                    user = User.objects.get(phone=self.user_phone)
                    django_login(request, user, "users.auth.UserAuthBackend")
                    request.session['phone'] = user.phone
                    return redirect("panel:dashboard")
                else:
                    form.add_error(None,"Invalid code entered")
                    return render(request, 'panel/user_verify.html', {'form': form})
            else:
                print("BUG?!")
                return redirect("panel:login")


@login_required
def logout(request):
    django_logout(request)
    request.session["authenticated"] = False
    request.session["phone"] = None
    request.session["user_phone"] = None
    return redirect("index")


@login_required(login_url="panel:login")
def dashboard_staff(request):
    orders = Order.objects.annotate(
        status_order=Case(
            When(status="Pending", then=Value(1)),
            When(status="Approved", then=Value(2)),
            When(status="Delivered", then=Value(3)),
            When(status="Rejected", then=Value(4)),
            When(status="Paid", then=Value(5)),
            # Add more cases for other choices
            default=Value(1),
            output_field=CharField(),
        )
    ).order_by('status_order')
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

    @method_decorator(login_required(login_url='panel:login'))
    def get(self, request, order_id:int):
        form =EditOrderForm(instance=self.order)
        item_forms = []
        for i in self.order_items:
            item_forms.append(EditOrderItemForm(instance=i, initial={"id":i.id}))
        add_item_form = AddOrderItemForm()

        context = {'form':form, 'order':self.order, 'orderitems':item_forms, "add_item_form":add_item_form}

        return render(request,'panel/dashboard_editoreder.html',context)

    @method_decorator(login_required(login_url='panel:login'))
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
        elif request.POST.get("add_item"):
            form = AddOrderItemForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                unit_price = cd["food"].price
                discount = cd["food"].discount
                item = OrderItem(
                    food=cd["food"],
                    quantity=cd["quantity"],
                    unit_price=unit_price,
                    discount=discount,
                    order=self.order,
                ).save()
        return redirect("panel:edit_order",order_id=order_id)



def simple_action(view_func):
    @login_required(login_url='panel:login')
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