# Generated by Django 2.1.7 on 2019-04-05 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0010_auto_20190402_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locations',
            name='avatar',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='locations',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='locations',
            name='longitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='locations',
            name='map',
            field=models.CharField(max_length=255, null=True),
        ),
    ]