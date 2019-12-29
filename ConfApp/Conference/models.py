from django.db import models
from Account.models import Account
from recoms.models import Theme

class Conference(models.Model):
    name = models.CharField(verbose_name="Conference name", default="Conference name",max_length=250, null=True)
    website = models.URLField(verbose_name="website", default='Conference.com', null=True)
    Start_date = models.DateTimeField(null=True)
    Finish_date = models.DateTimeField(null=True)
    Users = models.ManyToManyField(Account, related_name='conferences')
    Themes = models.ManyToManyField(Theme, related_name='conferences')


    def __str__(self):
        return self.name

# class general_msgs

    class Meta:
        permissions = (
            ('CED_sessions', "Create, Edite & Delete sessions"),
            ('edit_session', 'Edite specific session'),
            ('W2vec_training', "W2vec training"),
            ('Send_invitations', "Send invitations"),
            ('give_rights', "Give rights to users"),
            ('send_msg', "Send msgs to all conf users"),
            ('set_sessions_status', 'set session as ongoing, finished or not yet started by chairman')
        )