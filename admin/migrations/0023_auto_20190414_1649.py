# Generated by Django 2.1.7 on 2019-04-14 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0022_auto_20190414_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='collectionlocation',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Collections'),
        ),
        migrations.AddField(
            model_name='collectionlocation',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Locations'),
        ),
    ]
