# Generated by Django 4.0.2 on 2022-09-27 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0031_alter_electronic_address_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailrecord',
            name='status_message',
            field=models.TextField(),
        ),
    ]