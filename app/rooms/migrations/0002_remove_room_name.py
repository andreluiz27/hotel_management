# Generated by Django 4.2.3 on 2024-11-09 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='name',
        ),
    ]