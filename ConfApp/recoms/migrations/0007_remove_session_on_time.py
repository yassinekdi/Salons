# Generated by Django 2.2.5 on 2019-12-24 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recoms', '0006_session_on_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='on_time',
        ),
    ]
