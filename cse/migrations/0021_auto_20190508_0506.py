# Generated by Django 2.2 on 2019-05-08 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cse', '0020_auto_20190507_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='email',
            field=models.EmailField(default=None, max_length=254, unique=True),
        ),
    ]
