# Generated by Django 2.1.7 on 2019-03-25 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Categories')),
            ],
        ),
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
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentLikeShare',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255, null=True)),
                ('score', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CuisineLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisines',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InteractiveTypes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('address', models.CharField(max_length=255)),
                ('avatar', models.CharField(max_length=255)),
                ('map', models.CharField(max_length=255)),
                ('totalReview', models.BigIntegerField(null=True)),
                ('totalView', models.BigIntegerField(null=True)),
                ('totalFavourite', models.BigIntegerField(null=True)),
                ('totalCheckin', models.BigIntegerField(null=True)),
                ('avgRating', models.FloatField(null=True)),
                ('priceMin', models.CharField(max_length=255, null=True)),
                ('priceMax', models.CharField(max_length=255, null=True)),
                ('workTime24h', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('keyWords', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(through='admin.CategoryLocation', to='admin.Categories')),
                ('cuisine', models.ManyToManyField(through='admin.CuisineLocation', to='admin.Cuisines')),
            ],
        ),
        migrations.CreateModel(
            name='MenuLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Locations')),
            ],
        ),
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('dishes', models.CharField(max_length=255)),
                ('displayOrder', models.BigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParkingLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Locations')),
            ],
        ),
        migrations.CreateModel(
            name='Parkings',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255, null=True)),
                ('map', models.CharField(max_length=255, null=True)),
                ('startTime24h', models.TimeField(null=True)),
                ('endTime24h', models.TimeField(null=True)),
                ('capacity', models.IntegerField(null=True)),
                ('capacityCar', models.IntegerField(null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Locations')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='servicelocation',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Services'),
        ),
        migrations.AddField(
            model_name='parkinglocation',
            name='parking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Parkings'),
        ),
        migrations.AddField(
            model_name='menulocation',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Menus'),
        ),
        migrations.AddField(
            model_name='locations',
            name='menu',
            field=models.ManyToManyField(through='admin.MenuLocation', to='admin.Menus'),
        ),
        migrations.AddField(
            model_name='locations',
            name='parking',
            field=models.ManyToManyField(through='admin.ParkingLocation', to='admin.Parkings'),
        ),
        migrations.AddField(
            model_name='locations',
            name='service',
            field=models.ManyToManyField(through='admin.ServiceLocation', to='admin.Services'),
        ),
        migrations.AddField(
            model_name='districts',
            name='provinceId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Provinces'),
        ),
        migrations.AddField(
            model_name='cuisinelocation',
            name='cuisine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Cuisines'),
        ),
        migrations.AddField(
            model_name='cuisinelocation',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Locations'),
        ),
        migrations.AddField(
            model_name='commentlikeshare',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Locations'),
        ),
        migrations.AddField(
            model_name='commentlikeshare',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.InteractiveTypes'),
        ),
        migrations.AddField(
            model_name='commentlikeshare',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
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
        migrations.AddField(
            model_name='categorylocation',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.Locations'),
        ),
    ]
