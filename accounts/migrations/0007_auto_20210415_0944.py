# Generated by Django 3.1.4 on 2021-04-15 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210415_0734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_student_approvee',
            new_name='is_student_approve',
        ),
    ]
