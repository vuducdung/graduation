# Generated by Django 2.1.7 on 2019-04-21 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_accounts_recommend_locs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='recommend_locs',
        ),
    ]