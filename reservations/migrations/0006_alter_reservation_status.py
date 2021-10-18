# Generated by Django 4.0a1 on 2021-10-13 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_remove_bookedday_created_remove_bookedday_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='pending', max_length=12),
        ),
    ]