# Generated by Django 2.1.7 on 2019-03-30 06:14

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0007_locations_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='news_tsv',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]