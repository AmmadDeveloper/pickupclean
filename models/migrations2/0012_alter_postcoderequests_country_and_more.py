# Generated by Django 4.0.4 on 2022-06-11 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0011_postcoderequests_postcode_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcoderequests',
            name='country',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='postcoderequests',
            name='email',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='postcoderequests',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]