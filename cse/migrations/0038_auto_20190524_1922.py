# Generated by Django 2.2 on 2019-05-24 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cse', '0037_auto_20190524_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalinfo',
            name='docotr_email',
        ),
        migrations.AddField(
            model_name='medicalinfo',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cse.Doctors'),
        ),
    ]
