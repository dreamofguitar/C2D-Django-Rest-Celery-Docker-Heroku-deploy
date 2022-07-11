# Generated by Django 3.0.8 on 2020-09-11 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0002_auto_20200826_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='appointment_reason',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cita',
            name='completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='cita',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='appointment_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
