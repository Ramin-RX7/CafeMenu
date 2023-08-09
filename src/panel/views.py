from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from orders.models import Order, Table, OrderItem
from .urls import *
from .forms import EditOrderForm, EditOrderItemForm



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