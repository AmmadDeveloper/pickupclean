# Generated by Django 4.0.4 on 2022-08-04 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0018_notification_alter_cart_category_alter_cart_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='heading',
            field=models.CharField(default='', max_length=100),
        ),
    ]
