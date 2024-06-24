# Generated by Django 5.0.1 on 2024-06-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_communications_comm_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('badge', models.CharField(max_length=20)),
                ('created_by', models.CharField(max_length=20)),
                ('created_on', models.DateTimeField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Contractors',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='communications',
            name='parent_id',
            field=models.IntegerField(default=0),
        ),
    ]
