from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView

from foods.models import Food
from users.models import User
from .models import Order,Table,OrderItem
from .forms import CustomerLoginForm



def index(request):
    current_session_orders_ids = request.session.get('orders', [])
    current_session_orders = Order.objects.filter(id__in=current_session_orders_ids)
    context = {
        'orders' : current_session_orders
    }
    return render(request,'orders/order_list.html',context)


def order_list(request):
    return redirect("index")


def order_details(request,id):
    session_id=request.session['orders']
    order = get_object_or_404(Order, id=session_id[id-1])
    context = {"order": order}
    return render(request,'orders/order_details.html',context)


class SetOrderView(View):

    def post(self, request):
        if not (data := request.COOKIES.get("cart")):
            redirect("orders:cart")
        cart = eval(data)
        customer = request.session.get("phone")
        if not customer:
            if isinstance(request.user, User):
                customer = request.user.phone
            else:
                redirect("index")
        discount = 0.0
        table = Table.get_available_table()

        order = Order(customer=customer, table=table, discount=discount)

        response = redirect("orders:index")
        with transaction.atomic():
            order.save(check_items=False)
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




def cart(request):
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

class CartAddView(View):
    def get(self, request):
        return redirect("foods:menu")

    def post(self, request):
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



class CartDeleteView(RedirectView):
    def post(self, request, *args, **kwargs):
        data = request.COOKIES.get("cart")
        cart = eval(data)
        food_id = request.POST["food"]
        del cart[food_id]
        str_cart = str(cart)
        response = redirect('orders:cart')
        response.set_cookie('cart', str_cart)
        return response



class CustomerLoginView(View):
    def post(self,request):
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            request.session['phone'] = phone
        else:
            import main.utils
            main.utils.EditableContexts.form_login_error = "Invalid phone number"
        return redirect(request.META.get('HTTP_REFERER', reverse('index')))
