# Generated by Django 4.2.3 on 2023-07-10 15:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('airport_app', '0002_alter_airplane_airplane_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='airplane',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]