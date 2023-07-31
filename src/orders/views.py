from datetime import datetime

from django.shortcuts import render,redirect
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect

from .models import Order,Table,OrderItem
from .forms import CustomerLoginForm
from foods.models import Food

# Create your views here.

def index(request):
    orders  = Order.objects.all()
    context = {"orders": orders }
    return render(request,'orders/order_list.html',context)
def order_list(request):
    return redirect("index")


def order_details(request,id):
    order = Order.objects.get(id=id)
    context = {"order": order}
    return render(request,'orders/order_details.html',context)


def set_order(request):
    if request.method == "POST":
        if not (data := request.COOKIES.get("cart")):
            redirect("cart")
        cart = eval(data)
        customer = request.session.get("phone")

        discount = 0.0
        date_submit = datetime.now()
        table = Table.get_available_table()

        order = Order(customer=customer, table=table, discount=discount, date_submit=date_submit)
        items = []

        with transaction.atomic():
            order.save(check_price=False)
            for food_id,quantity in cart.items():
                food = Food.objects.get(id=food_id)
                orderitem = OrderItem(
                    order = order,
                    food = food,
                    quantity = quantity,
                    unit_price = food.price,
                    discount = food.discount
                )
                orderitem.save()
                items.append(orderitem)

    return redirect("orders:index")


def cart(request):
    if request.method == "GET":
        data = request.COOKIES.get("cart")
        cart = eval(data)
        new_cart = {}
        for key,value in cart.items():
            food = Food.objects.get(id=key)
            new_cart[food] = value
        context = {"cart": new_cart}
        return render(request,'orders/cart.html',context)


def cart_delete(request):
    if request.method =="POST":
        data = request.COOKIES.get("cart")
        food_id = request.POST["food"]
        cart = eval(data)
        del cart[food_id]
        str_cart = str(cart)
        response = redirect('cart')
        response.set_cookie('cart', str_cart)
        return response
    return redirect('cart')


def customer_login(request):
    if request.method == "POST":
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            phone=form.cleaned_data['phone']
            request.session['phone']=phone
    return redirect('menu.html')
