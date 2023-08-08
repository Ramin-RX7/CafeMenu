from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order, Table, OrderItem
from .urls import *
from .forms import EditOrderForm, EditOrderItemForm

# Create your views here.

def dashboard_staff(request):
    orders = Order.objects.order_by('status')
    tables = Table.objects.all()
    context = {
        'orders': orders,
        'tables': tables,
    }
    return render(request,'panel/dashboard_staff.html', context)


def edit_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = order.orderitem_set.all()
    if request.method == "POST":
        formitem = EditOrderItemForm(request.POST)
        for i in request.POST:
            print(i)
        if formitem.is_valid():
            clean_d=formitem.cleaned_data
            print(clean_d)
            # orderitem_id = clean_d['orderitem__id']
            # orderitem=OrderItem.objects.get(id=orderitem_id)
            # form = EditOrderForm(request.POST, instance=order)
            # formitem.save()
            # form_item = EditOrderItemForm(request.POST, instance=order_items)
            # if form.is_valid():
                # Order.objects.update(form)
                # return redirect('dashboard')
        # elif form_item.is_valid():
            # form_item.save()

    form =EditOrderForm(instance=order)
    formitems = []
    for i in order_items:
        formitems.append(EditOrderItemForm(instance=i, initial={"id":i.id}))

    context = {'form':form,'order':order, 'orderitems':formitems}

    return render(request,'panel/dashboard_editoreder.html',context)


def simple_action(view_func):
    def _wrapped_view(request, order_id, *args, **kwargs):
        response = view_func(request, order_id, *args, **kwargs)
        return redirect('panel:dashboard')
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