# Generated by Django 4.1 on 2022-08-05 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aivisa_engine', '0003_photo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.TextField(default='', max_length=1024),
        ),
    ]
