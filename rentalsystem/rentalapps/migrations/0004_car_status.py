# Generated by Django 4.2.9 on 2024-02-03 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapps', '0003_remove_booking_ending_day_booking_no_of_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='status',
            field=models.CharField(blank=True, default='Available', max_length=20, null=True),
        ),
    ]
