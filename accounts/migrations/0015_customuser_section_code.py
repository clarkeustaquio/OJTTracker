# Generated by Django 3.1.4 on 2021-04-21 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_customuser_school_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='section_code',
            field=models.CharField(default='None', max_length=150),
        ),
    ]