# Generated by Django 3.1.4 on 2021-04-21 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_customuser_is_switch'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='school_name',
            field=models.CharField(default='New Era', max_length=150),
        ),
    ]
