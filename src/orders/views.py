import json

from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
from django.urls import reverse
from django.views import View
from django.views.generic import ListView,DetailView,RedirectView

from foods.models import Food
from users.models import User
from .models import Order,Table,OrderItem
from .forms import CustomerLoginForm


class IndexView(ListView):
    model=Order
    template_name= 'orders/order_list.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        current_session_orders_ids=self.request.session.get('orders',[])
        context['orders'] = Order.objects.filter(id__in=current_session_orders_ids)
        return context


class OrderListView(RedirectView):
    pattern_name = 'orders:index'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_details.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        session_id = self.request.session.get('orders')
        order_id = int(self.kwargs.get('id')) - 1
        order = get_object_or_404(Order, id=session_id[order_id])
        return order


class SetOrderView(View):
    def post(self, request):
        data = request.POST.get("cart_data")
        if not data:
            return redirect("orders:cart")
        customer = request.session.get("phone")
        if not customer:
            if isinstance(request.user, User):
                customer = request.user.phone
            else:
                redirect("orders:cart")

        data = json.loads(data)
        discount = 0.0
        table = Table.get_available_table()

        order = Order(customer=customer, table=table, discount=discount)

        with transaction.atomic():
            order.save(check_items=False)
            for food_id,quantity in data.items():
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

        response = redirect("orders:index")
        response.delete_cookie("cart")
        return response




def cart(request):
    data = request.GET.get("cart_data") or {}
    cart = {}
    cart_given = False
    if data:
        cart_given = True
        if (data:=json.loads(data)):
            for food_id,quantity in data.items():
                food = Food.objects.get(id=food_id)
                cart[food] = quantity

    context = {"cart": cart, "cart_given":cart_given}
    return render(request,'orders/cart.html',context)


class CartAddView(View):
    def post(self, request):
        if (food_id := request.POST.get('change')):
            quantity = request.POST.get('quantity')
            cart_cookie = request.COOKIES.get('cart')
            if cart_cookie:
                cart_dict = eval(cart_cookie)
            else:
                cart_dict= {}

            cart_dict[food_id] = quantity
            response = redirect('orders:cart')
            response.set_cookie('cart', str(cart_dict))
            return response
        elif (food_id := request.POST.get('food')):
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
    pattern_name = "orders:cart"
    def post(self, request, *args, **kwargs):
        data = request.COOKIES.get("cart")
        cart = eval(data)
        food_id = request.POST["food"]
        del cart[food_id]
        str_cart = str(cart)
        response = redirect(self.pattern_name)
        response.set_cookie('cart', str_cart)
        return response



class CustomerLoginView(View):
    def post(self,request):
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            request.session['phone'] = phone
        else:
            import core.utils
            core.utils.EditableContexts.form_login_error = "Invalid phone number"
        return redirect(request.META.get('HTTP_REFERER', reverse('index')))
