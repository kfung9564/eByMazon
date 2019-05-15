# Generated by Django 2.2 on 2019-05-14 20:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20190514_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='picture',
            field=models.URLField(validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]
