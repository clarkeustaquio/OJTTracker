# Generated by Django 3.1.4 on 2021-04-15 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210415_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='answer',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_male',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='question',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]