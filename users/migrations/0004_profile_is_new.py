# Generated by Django 2.2 on 2019-05-13 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190507_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]
