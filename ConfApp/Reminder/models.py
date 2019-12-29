from django.db import models
from recoms.models import Session
from Account.models import Account

#
# class Reminder(models.Model):
#
#     Sessions = models.ManyToManyField(Session,related_name='reminder_sessions', null=True)
#     # Users = models.ManyToManyField(Account,related_name="reminder_users", null=True)
#
#     def __str__(self):
#         return self.Sessions
