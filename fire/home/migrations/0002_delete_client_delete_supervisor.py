# Generated by Django 4.1.7 on 2023-04-03 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='client',
        ),
        migrations.DeleteModel(
            name='supervisor',
        ),
    ]
