# Generated by Django 2.1.7 on 2019-04-24 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_accounts_recommend_locs'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='recommend_locs',
            field=models.TextField(default=''),
        ),
    ]