# Generated by Django 3.1.4 on 2021-04-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_customuser_section_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_confirm_employer',
            field=models.BooleanField(default=False),
        ),
    ]
