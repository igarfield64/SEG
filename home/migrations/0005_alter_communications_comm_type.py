# Generated by Django 5.0.1 on 2024-03-03 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_todo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communications',
            name='comm_type',
            field=models.IntegerField(choices=[(0, 'Inbound'), (1, 'Outbound')]),
        ),
    ]