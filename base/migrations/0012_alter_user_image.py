# Generated by Django 5.1.5 on 2025-02-12 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='images/'),
        ),
    ]
