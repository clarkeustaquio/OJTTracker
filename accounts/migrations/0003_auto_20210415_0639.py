# Generated by Django 3.1.4 on 2021-04-15 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210415_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='pending_employee',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='pending_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
