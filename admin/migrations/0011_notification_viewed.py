# Generated by Django 2.1.7 on 2019-05-09 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0010_auto_20190509_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
