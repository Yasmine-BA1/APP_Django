# Generated by Django 4.1.7 on 2023-03-26 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='position',
        ),
        migrations.RemoveField(
            model_name='supervisor',
            name='position',
        ),
    ]
