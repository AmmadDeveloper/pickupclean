# Generated by Django 4.0.4 on 2022-07-28 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='purchased',
            field=models.BooleanField(default=False),
        ),
    ]