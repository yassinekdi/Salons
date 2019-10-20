from django.db import models
from ConfApp.utils import unique_slug_messaging_generator
from Account.models import Account
from django.db.models.signals import pre_save


class Message(models.Model):
    sender = models.ForeignKey(Account,related_name="messages",on_delete=models.SET_NULL,null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.first_name + ' ' + self.sender.last_name


class Discussion(models.Model):
    participants = models.ManyToManyField(Account,related_name="discussions",blank=True)
    slug = models.SlugField(max_length=250, null=True,blank=True)
    messages = models.ManyToManyField(Message,blank=True)

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

    def __str__(self):
        return "{}".format(self.pk)


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_messaging_generator(instance)


pre_save.connect(slug_generator,sender=Discussion)


