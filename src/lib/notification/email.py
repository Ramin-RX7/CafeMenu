from django.core.mail import EmailMessage, send_mass_mail

from config.settings import DEFAULT_FROM_EMAIL
from users.models import User
from .notification import BaseNotification



class EmailNotification(BaseNotification):
    """
    Email Notfication (Base) class.
    """

    def send(self, user, body=None) -> dict:
        data = self.get_notification_data()
        body = body or self.get_message(user)
        email = EmailMessage(
            subject=data["subject"], body=body, to=[user]
        )
        email.send()

    def get_message(self, user: User):
        return f"""
            Hey {user.username}!\n
            {self.get_notification_data()}
        """

    def send_bulk(self, users: list[User] = None, body=None):
        """This function can be resource heavy specially when message is too long"""
        users = users or self.users
        data = self.get_notification_data()
        emails = []
        for user in users:
            body = body or self.get_message(user)
            emails.append((
                data["subject"],
                body,
                DEFAULT_FROM_EMAIL,
                [user.email],
            ))
        count = send_mass_mail(emails)
        # XXX: check if count = len(users)
