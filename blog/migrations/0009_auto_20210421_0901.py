# Generated by Django 3.1.4 on 2021-04-21 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210421_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='section_code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
