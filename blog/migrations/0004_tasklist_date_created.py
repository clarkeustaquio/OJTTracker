# Generated by Django 3.1.4 on 2021-04-17 10:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210415_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
