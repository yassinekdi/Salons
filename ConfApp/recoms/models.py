from django.db import models
from Account.models import Account


class Theme(models.Model):
    room = models.CharField(verbose_name='room', max_length=50, default="room")
    title = models.CharField(verbose_name="title", max_length=50, default="title")


    def __str__(self):
        return self.title

class SubTheme(models.Model):
    title = models.CharField(verbose_name="title", max_length=50, default="title")
    Theme = models.ForeignKey(Theme, related_name='subtheme', on_delete=models.SET_NULL, null=True)
    exists = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Session(models.Model):

    Status_choice = (('Not yet', 'Not yet'), ('Ongoing', 'Ongoing'), ('Finished', 'Finished'))

    # Authors = models.ManyToManyField(Account, related_name="session")
    # Speakers = models.ManyToManyField(Account, related_name="session")
    Authors = models.CharField(verbose_name="authors", max_length=50, default="authors")
    Speakers = models.CharField(verbose_name="authors", max_length=50, default="authors")
    Title = models.CharField(verbose_name="title", max_length=50, default="title")
    Start_time = models.DateTimeField(null=True)
    Start_timeC = models.CharField(verbose_name='Start time', max_length=20, null=True)
    Final_time = models.DateTimeField(null=True)
    Final_timeC = models.CharField(verbose_name='Final time', max_length=20, null=True)
    Room = models.CharField(verbose_name="room", max_length=50, default="room")
    Theme = models.ForeignKey(Theme, related_name='sessions' ,on_delete=models.SET_NULL, null=True)
    Abstract = models.CharField(verbose_name="title", max_length=300, default="abstract")
    Status = models.CharField(verbose_name="Status", max_length=20, choices=Status_choice, null=True)
    Recommended = models.BooleanField(default=False)
    Reminded_users = models.ManyToManyField(Account, related_name='reminded_sessions')



    def __str__(self):
        return self.Title




