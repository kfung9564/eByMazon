# Generated by Django 2.1.7 on 2019-05-07 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190418_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='credit_card_num',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_num',
            field=models.PositiveIntegerField(default=0),
        ),
    ]