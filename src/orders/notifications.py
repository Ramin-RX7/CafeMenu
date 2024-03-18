import json

from lib.notification import EmailNotification
from interactions.models import Notification, UserNotification
from orders.models import Order
from users.models import User



class OrderNotification:
    notification_class = EmailNotification

    @staticmethod
    def get_client_name(user:User):
        return user.first_name or user.last_name or user.phone

    def get_notifications(self, name:str, order:Order):
        notification_row = Notification.objects.create(
            name = name,
            data = json.dumps({
                "order_id": order.id
            })
        )

        usernotification_row = UserNotification.objects.create(
            user = order.customer,
            notification = notification_row,
        )

        notification_obj = self.notification_class(
            notification_row,
            [User.objects.get(id=order.customer.id)]
        )

        return (notification_row, usernotification_row, notification_obj)

    def send(self, order:Order, body:str):
        customer = order.customer
        ntf_row, user_ntf_row, ntf_obj = self.get_notifications("order_ready", order)

        ntf_obj.send(customer, body=body)

        ntf_row.is_sent = True
        ntf_row.save()
        user_ntf_row.save()

    def order_ready(self, order:Order):
        body = f"""\
            Dear {self.__class__.get_client_name()}, Your order is ready!
        """
        self.send(order, body)

    def order_rejected(self, order:Order, reason:str=""):
        body = f"""\
            Dear {self.__class__.get_client_name()}, Your order is rejected!
            Reason: {reason}
        """
        self.send(order, body)
