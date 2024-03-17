import json
from datetime import datetime, timedelta
from django.http import JsonResponse

from django.shortcuts import render,redirect
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
        context['orders'] = Order.objects.filter(customer=self.request.user).order_by("-created_at")
        return context


class OrderListView(RedirectView):
    pattern_name = 'orders:index'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_details.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("orders:index")
        t = self.kwargs.get("datetime")
        interval = timedelta(seconds=1)
        orders = Order.objects.filter(
            customer = user,
            created_at__lte = datetime.strptime(t, "%Y%m%d%H%M%S") + interval,
            created_at__gte = datetime.strptime(t, "%Y%m%d%H%M%S") - interval,
        )
        if orders.exists():
            return orders.get()



class SetOrderView(View):
    def post(self, request):
        body = json.loads(request.body)
        data = body.get("cart")
        table_id = body.get("table")
        customer:User = request.user
        if not all([customer.is_authenticated,data,table_id]):
            return redirect("orders:cart")

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
        return JsonResponse({}, status=200)


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
