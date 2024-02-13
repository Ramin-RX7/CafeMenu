from django.db import models

from core.models import BaseModel
from users.models import User



class Notification(BaseModel):
    name = models.CharField(max_length=75)
    data = models.TextField()
    is_sent = models.BooleanField(default=False)

    def add_user(self, users: list[User]):
        user_notifications = [
            UserNotification(user=user, notification=self) for user in users
        ]
        UserNotification.objects.bulk_create(user_notifications)


class UserNotification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT)
    # TODO: is_received & is_read columns
