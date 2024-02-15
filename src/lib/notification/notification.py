import json
from abc import ABC, abstractmethod

from users.models import User
from interactions.models import Notification, UserNotification



class BaseNotification(ABC):
    def __init__(self, notification: Notification, users: list[User] = []):
        self.notification = notification
        self.data = self.get_notification_data()
        self.users = users

    def pre_send(self, user, **kwargs) -> dict:
        """Called before sending notification to a user"""
        ...

    @abstractmethod
    def send(self, user, **kwargs) -> dict:
        """
        Called when all preparation is done and notification execution time is reached
        """
        ...

    def post_send(self, user, **kwargs) -> dict:
        """Called after notification is sent to a user"""
        ...

    def send_to_user(self, user, **pre_send_kwargs):
        """Implements the notification sending route"""
        pre_send_data = self.pre_send(user, **pre_send_kwargs) or {}
        send_data = self.send(user, **pre_send_data) or {}
        return self.post_send(user, **send_data) or send_data

    def send_all(self, users: list[User] = None):
        """Sends the notification to all users"""
        users = users or self.users
        for user in users:
            self.send_to_user(user)
        self.finalize_send()

    def send_bulk(self, users: list[User] = None):
        """Bulk send notification.
        Useful for situations where multiple notifications can be sent through one connection.
        By default runs self.send_bulk(users)
        """
        return self.send_all(users)  # XXX: or raise NotImplementedError

    def create_user_notification(self, user):
        """Create notification for given user"""
        return UserNotification(user=user, notification=self.notification)
        # TODO: get_or_create_user_notification
        #  (using self.usernotifications: dict[user_id, UserNotification])

    def get_notification_data(self):
        """Get data from self.notification.data"""
        return json.loads(self.notification.data)

    def finalize_send(self):
        """Finalize the notification sending proceess.
        Must be called fter notificaion is sent to all users
        """
        self.notification.is_sent = True
        self.notification.save()
