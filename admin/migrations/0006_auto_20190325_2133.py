# Generated by Django 2.1.7 on 2019-03-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0005_auto_20190325_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menus',
            name='dishes',
            field=models.TextField(default=''),
        ),
    ]