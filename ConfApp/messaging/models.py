from django.db import models
from Account.models import Account


class Discussion(models.Model):
    slug = models.SlugField(max_length=250, null=True,blank=True)
    # participants = models.ManyToManyField(Account,related_name="discussions", blank=True)


class Message(models.Model):
    sender = models.ForeignKey(Account,related_name="messages",on_delete=models.SET_NULL,null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    discussion = models.ForeignKey(Discussion,related_name="messages",on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sender.first_name + ' ' + self.sender.last_name





    def __str__(self):
        return "{}".format(self.pk)



