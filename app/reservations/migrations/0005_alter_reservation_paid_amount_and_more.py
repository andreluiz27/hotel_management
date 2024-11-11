# Generated by Django 4.2.3 on 2024-11-10 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_alter_room_room_type'),
        ('reservations', '0004_reservation_check_in_reservation_check_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='paid_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('Cash', 'Cash'), ('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Pix', 'Pix')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payment_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Pendent', 'Pendent')], default='Pendent', max_length=255),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_status',
            field=models.CharField(blank=True, choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('On Hold', 'On Hold'), ('Checked In', 'Checked In'), ('Checked Out', 'Checked Out')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rooms.room'),
        ),
    ]