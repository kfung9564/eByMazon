# Generated by Django 2.2 on 2019-05-15 08:58

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='itemapplication',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidDate',
            field=models.DateTimeField(blank=True, verbose_name=datetime.datetime(2019, 5, 15, 8, 58, 57, 844176, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidPrice',
            field=models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='uploadDate',
            field=models.DateTimeField(blank=True, verbose_name=datetime.datetime(2019, 5, 15, 8, 58, 57, 843160, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='itembidprice',
            name='startDate',
            field=models.DateTimeField(blank=True, verbose_name=datetime.datetime(2019, 5, 15, 8, 58, 57, 844176, tzinfo=utc)),
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
        migrations.AlterField(
            model_name='order',
            name='orderDate',
            field=models.DateTimeField(blank=True, verbose_name=datetime.datetime(2019, 5, 15, 8, 58, 57, 844176, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='bid',
            unique_together=set(),
        ),
    ]
