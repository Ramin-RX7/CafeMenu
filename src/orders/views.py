from datetime import datetime

from django.shortcuts import render,redirect
from django.db import transaction
from django.urls import reverse

from .models import Order,Table,OrderItem
from .forms import CustomerLoginForm
from foods.models import Food

# Create your views here.

def index(request):
    current_session_orders_ids = request.session.get('orders', [])
    current_session_orders = []
    for order_id in current_session_orders_ids:
        try:
            order = Order.objects.get(id=order_id)
            current_session_orders.append(order)
        except Order.DoesNotExist:
            pass
    context = {
        'orders' : current_session_orders
    }

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
            redirect("orders:cart")
        cart = eval(data)
        customer = request.session.get("phone")
        discount = 0.0
        table = Table.get_available_table()

        order = Order(customer=customer, table=table, discount=discount)

        response = redirect("orders:index")
        with transaction.atomic():
            order.save(check_price=False)
            for food_id,quantity in cart.items():
                food = Food.objects.get(id=food_id)
                orderitem = OrderItem(
                    order = order,
                    food = food,
                    quantity = int(quantity),
                    unit_price = food.price,
                    discount = food.discount
                )
                orderitem.save()
            session_orders = request.session.get("orders", [])
            session_orders.append(order.id)
            request.session["orders"] = session_orders

        response.delete_cookie("cart")
        return response

    return redirect("orders:index")


def cart(request):
    if request.method == "POST":  # moved to cart_add()
        food_id = request.POST.get('food')
        quantity = request.POST.get('quantity')
        cart_cookie = request.COOKIES.get('cart')

        if cart_cookie:
            cart_dict = eval(cart_cookie)
        else:
            cart_dict= {}

        cart_dict[food_id] = quantity
        response = redirect('foods:menu')
        response.set_cookie('cart', str(cart_dict))
        return response

    data = request.COOKIES.get("cart")
    if not (data := request.COOKIES.get("cart")):
        return render(request,'orders/cart.html',{})
    cart = eval(data)
    new_cart = {}
    for key,value in cart.items():
        food = Food.objects.get(id=key)
        new_cart[food] = value
    if new_cart == {}:
        context = {}
    else:
        context = {"cart": new_cart}
    return render(request,'orders/cart.html',context)


def cart_add(request):
    if request.method == "POST":
        food_id = request.POST.get('food')
        quantity = request.POST.get('quantity')
        cart_cookie = request.COOKIES.get('cart')
        if cart_cookie:
            cart_dict = eval(cart_cookie)
        else:
            cart_dict= {}

        cart_dict[food_id] = quantity
        response = redirect('foods:menu')
        response.set_cookie('cart', str(cart_dict))
        return response
    return redirect("foods:menu")

def cart_delete(request):
    if request.method =="POST":
        data = request.COOKIES.get("cart")
        cart = eval(data)
        food_id = request.POST["food"]
        del cart[food_id]
        str_cart = str(cart)
        response = redirect('orders:cart')
        response.set_cookie('cart', str_cart)
        return response
    return redirect('orders:cart')


def customer_login(request):
    if request.method == "POST":
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            request.session['phone'] = phone
        else:
            import main.utils
            main.utils.EditableContexts.form_login_error = "Invalid phone number"

    return redirect(request.META.get('HTTP_REFERER', reverse('index')))
