# Generated by Django 5.1.5 on 2025-01-31 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=80)),
            ],
        ),
        migrations.AlterField(
            model_name='list',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.topic'),
        ),
    ]
