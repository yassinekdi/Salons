# Generated by Django 2.2.5 on 2019-12-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recoms', '0007_remove_session_on_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='Reminded',
            field=models.BooleanField(default=False),
        ),
    ]
