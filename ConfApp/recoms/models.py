from django.db import models
from Account.models import Account


class Session(models.Model):
    # authors = models.ManyToManyField(Account, related_name="session")
    authors = models.CharField(verbose_name="authors", max_length=50, default="authors")
    title = models.CharField(verbose_name="title", max_length=50, default="title")
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title