# Generated by Django 2.2.5 on 2020-01-19 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recoms', '0014_topic_exists'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='title', max_length=50, verbose_name='title')),
                ('exists', models.BooleanField(default=False)),
                ('Theme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subtheme', to='recoms.Theme')),
            ],
        ),
        migrations.DeleteModel(
            name='topic',
        ),
    ]
