# Generated by Django 2.2.5 on 2019-11-17 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0014_auto_20191117_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notif_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL),
        ),
    ]
