# Generated by Django 2.1.7 on 2019-03-25 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_auto_20190325_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='district',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, to='admin.Districts'),
        ),
    ]