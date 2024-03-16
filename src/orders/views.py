import json

from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
from django.views import View
from django.views.generic import ListView,DetailView,RedirectView
from django.core.cache import caches

from foods.models import Food
from users.models import User
from .models import Order,Table,OrderItem



AUTH_CACHE = caches["default"]


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
        data = request.COOKIES.get("cart")
        table_id = request.COOKIES.get("table")
        if not all([data,table_id]):
            return redirect("orders:cart")

        customer = request.session.get("phone")
        if not customer:
            if isinstance(request.user, User):
                customer = request.user.phone
            else:
                redirect("orders:cart")

        data = json.loads(data)
        discount = 0.0
        table = Table.objects.get(id=int(table_id))

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
        if len(request.session.get("orders", [])):
            response = redirect("orders:order_details", len(request.session.get("orders", [])))
            response.delete_cookie("cart")
        else:
            response = redirect("order:cart")
        return response




def cart(request):
    data = request.COOKIES.get("cart") or {}
    cart = {}
    cart_given = False
    if data:
        cart_given = True
        if (data:=json.loads(data)):
            for food_id,quantity in data.items():
                food = Food.objects.get(id=food_id)
                cart[food] = quantity
        del request.COOKIES["cart"]
    context = {"cart": cart, "cart_given":cart_given, "tables":Table.objects.all()}
    response = render(request, 'orders/cart.html', context)
    response.delete_cookie('cart')
    return response
