# Generated by Django 3.0.8 on 2020-09-28 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twtesttoken',
            name='room',
            field=models.CharField(max_length=500),
        ),
    ]