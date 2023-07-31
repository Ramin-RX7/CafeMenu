from django.shortcuts import render,redirect

from .models import Order
from foods.models import Food


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