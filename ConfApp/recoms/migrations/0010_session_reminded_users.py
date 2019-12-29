# Generated by Django 2.2.5 on 2019-12-26 19:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recoms', '0009_remove_session_reminded'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='Reminded_users',
            field=models.ManyToManyField(null=True, related_name='reminded_sessions', to=settings.AUTH_USER_MODEL),
        ),
    ]
