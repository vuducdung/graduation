# Generated by Django 2.1.7 on 2019-05-27 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_uploadavatarimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadavatarimage',
            name='avatar',
            field=models.ImageField(upload_to='avatar/'),
        ),
    ]
