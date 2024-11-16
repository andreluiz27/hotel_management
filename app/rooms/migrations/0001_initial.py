# Generated by Django 4.2.3 on 2024-11-16 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('room_status', models.CharField(choices=[('Available', 'Available'), ('Occupied', 'Occupied'), ('Maintenance', 'Maintenance'), ('Cleaning', 'Cleaning'), ('Out of Service', 'Out of Service')])),
                ('floor', models.IntegerField()),
                ('room_type', models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Luxury Single', 'Luxury Single'), ('Luxury Double', 'Luxury Double')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
