# Generated by Django 2.1.7 on 2019-04-21 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_location',
            name='rating',
            field=models.FloatField(null=True),
        ),
    ]
