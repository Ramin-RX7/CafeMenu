from django.db.models import Case, CharField, Value, When
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View

from orders.models import Order, Table, OrderItem
from ..urls import *
from ..forms import EditOrderForm, EditOrderItemForm, AddOrderItemForm




@login_required(login_url="panel:login")
def dashboard(request):
    ALL_ORDERS = Order.objects.all()
    orders = ALL_ORDERS.annotate(
        status_order=Case(
            When(status="Pending", then=Value(1)),
            When(status="Approved", then=Value(2)),
            When(status="Delivered", then=Value(3)),
            When(status="Rejected", then=Value(4)),
            When(status="Paid", then=Value(5)),
            default=Value(1),
            output_field=CharField(),
        )
    ).order_by('status_order')
    tables = Table.objects.all()
    context = {
        'orders': orders,
        'orders_by_date': ALL_ORDERS,
        'orders_user': ALL_ORDERS.filter(responsible_staff=request.user),
        'tables': tables,
        "name": request.user.first_name,
    }
    return render(request,'panel/dashboard.html', context)



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
        # update order main info
        if request.POST.get("order"):
            form = EditOrderForm(request.POST, instance=self.order)
            if form.is_valid():
                form.save()
                return redirect("panel:dashboard")
            else:
                form.add_error(None,"Invalid input")
        # update order items
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
        # add new item
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
    order.take_responsibility(request.user)

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

@simple_action
def take_responsibility(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.take_responsibility(request.user)
