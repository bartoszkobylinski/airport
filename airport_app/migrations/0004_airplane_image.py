# Generated by Django 4.2.3 on 2023-07-11 18:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airport_app', '0003_airplane_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='airplane',
            name='image',
            field=models.ImageField(default=datetime.datetime(2023, 7, 11, 18, 31, 25, 226667, tzinfo=datetime.timezone.utc), upload_to='airport_app_images/'),
            preserve_default=False,
        ),
    ]
