from django.contrib.postgres.search import SearchVectorField
from django.db import models

from app.models import Accounts


# Create your models here.

class Provinces(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    latitude = models.FloatField(default=21.033333)
    longitude = models.FloatField(default=105.850000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Districts(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    provinceId = models.ForeignKey(Provinces, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Menus(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    dishes = models.TextField(default='')
    displayOrder = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cuisines(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Parkings(models.Model):
    id = models.BigIntegerField(primary_key=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=True)
    map = models.CharField(max_length=255, null=True)
    startTime24h = models.TimeField(null=True)
    endTime24h = models.TimeField(null=True)
    capacity = models.IntegerField(null=True)
    capacityCar = models.IntegerField(null=True)
    description = models.CharField(max_length=255, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Services(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Categories(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InteractiveTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Locations(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=255, null=False)
    avatar = models.CharField(max_length=255, null=True)
    map = models.CharField(max_length=255, null=True)
    totalReview = models.BigIntegerField(default=0)
    totalView = models.BigIntegerField(default=0)
    totalFavourite = models.BigIntegerField(default=0)
    totalCheckin = models.BigIntegerField(default=0)
    avgRating = models.FloatField(default=0)
    priceMin = models.CharField(max_length=255, default='', null=True)
    priceMax = models.CharField(max_length=255, default='', null=True)
    workTime24h = models.CharField(max_length=255, default='', null=True)
    is_active = models.BooleanField(default=True)

    # timeStart24h = models.CharField(max_length=20, default='00:00 - 00:00')
    # timeEnd24h = models.CharField(max_length=20, default='00:00:00')
    # menu = models.TextField(null=True)
    url = models.CharField(max_length=255, default='')
    keyWords = models.CharField(max_length=255, default='', null=True)
    description = models.CharField(max_length=255, default='', null=True)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE, default=20)
    evaluation = models.CharField(max_length=255, default='[0,0,0,0,0,0]')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    menu = models.ManyToManyField(Menus, through='MenuLocation')
    parking = models.ManyToManyField(Parkings, through='ParkingLocation')
    service = models.ManyToManyField(Services, through='ServiceLocation')
    cuisine = models.ManyToManyField(Cuisines, through='CuisineLocation')
    category = models.ManyToManyField(Categories, through='CategoryLocation')

    news_tsv = SearchVectorField(null=True)


class CommentLikeShare(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    type = models.ForeignKey(InteractiveTypes, on_delete=models.CASCADE)
    content = models.TextField(max_length=255, null=True)
    score = models.FloatField(null=True)
    evaluation = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MenuLocation(models.Model):
    menu = models.ForeignKey(Menus, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CategoryLocation(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ParkingLocation(models.Model):
    parking = models.ForeignKey(Parkings, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ServiceLocation(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CuisineLocation(models.Model):
    cuisine = models.ForeignKey(Cuisines, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class uploadImage(models.Model):
    image = models.ImageField(upload_to='location/')


class Collections(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, null=True)
    location = models.ManyToManyField(Locations, through='CollectionLocation')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CollectionLocation(models.Model):
    collection = models.ForeignKey(Collections, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
