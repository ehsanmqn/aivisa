# Generated by Django 4.1 on 2022-08-05 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aivisa_engine', '0006_alter_photo_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='result',
            field=models.CharField(default='', max_length=1024),
        ),
    ]
