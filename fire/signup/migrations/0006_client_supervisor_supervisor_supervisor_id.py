# Generated by Django 4.1.7 on 2023-03-27 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0005_client_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='signup.supervisor'),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='supervisor_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]