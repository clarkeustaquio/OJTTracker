# Generated by Django 3.1.4 on 2021-04-15 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210414_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='is_employee_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tasklist',
            name='is_send',
            field=models.BooleanField(default=False),
        ),
    ]
