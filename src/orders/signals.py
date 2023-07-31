from django.db.models.signals import post_save,pre_init
from django.dispatch import receiver

from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def handle_orderItem_save(sender, instance, created, **kwargs):
    if created:
        if instance.order is not None:
            order_instance = instance.order
            order_instance.price = sum([item.quantity*item.food.price for item in order_instance.orderitem_set.all()])
            order_instance.save()
            print("Order price updated by", instance)
