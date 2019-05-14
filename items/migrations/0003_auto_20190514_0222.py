# Generated by Django 2.2 on 2019-05-14 02:22

import django.core.validators
from django.db import migrations, models
import items.models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20190513_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bidPrice',
            field=models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='itembidprice',
            name='endDate',
            field=models.DateTimeField(validators=[items.models.validate_date]),
        ),
        migrations.AlterField(
            model_name='itembidprice',
            name='startPrice',
            field=models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='itemfixedprice',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]