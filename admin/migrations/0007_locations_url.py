# Generated by Django 2.1.7 on 2019-03-27 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0006_auto_20190325_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='url',
            field=models.CharField(default='', max_length=255),
        ),
    ]
