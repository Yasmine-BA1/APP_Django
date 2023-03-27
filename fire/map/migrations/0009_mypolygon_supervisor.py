# Generated by Django 4.1.7 on 2023-03-27 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0006_client_supervisor_supervisor_supervisor_id'),
        ('map', '0008_remove_mypolygon_author_mypolygon_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypolygon',
            name='supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='signup.supervisor'),
        ),
    ]