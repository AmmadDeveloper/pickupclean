# Generated by Django 4.0.2 on 2022-10-31 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0034_phonecode_emailcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailrecord',
            name='status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='messagerecord',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='dropoff_time_slot',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='pickup_time_slot',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='phonecode',
            name='code',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='postal_address',
            name='type',
            field=models.CharField(choices=[('Home', 'Home'), ('Billing', 'Billing'), ('Shipping', 'Shipping')], default='Home', max_length=20),
        ),
        migrations.AlterField(
            model_name='postcoderequests',
            name='country',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='promo',
            name='code',
            field=models.CharField(max_length=20),
        ),
    ]
