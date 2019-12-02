from django.db import models
from Account.models import Account


class Discussion(models.Model):
    slug = models.SlugField(max_length=250, null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.slug


class Message(models.Model):
    sender = models.ForeignKey(Account,related_name="messages",on_delete=models.SET_NULL,null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    discussion = models.ForeignKey(Discussion,related_name="messages",on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sender.first_name + ' ' + self.sender.last_name

class Notification(models.Model):
    notif_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notification')
    notif_discussion = models.CharField(max_length=50, null=True)
    notif_read = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.id)