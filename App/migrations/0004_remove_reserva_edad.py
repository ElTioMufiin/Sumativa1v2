# Generated by Django 4.2.4 on 2023-11-22 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_reserva_edad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='edad',
        ),
    ]