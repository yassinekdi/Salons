# Generated by Django 2.2.5 on 2019-10-20 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='participants',
        ),
        migrations.AlterField(
            model_name='discussion',
            name='messages',
            field=models.ManyToManyField(blank=True, related_name='messages', to='messaging.Message'),
        ),
    ]
