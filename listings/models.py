from django.db import models

# Table columns: id,street,status,price,bedrooms,bathrooms,sq_ft,lat,lng
class House(models.Model):
    id = models.CharField(primary_key = True, max_length = 40)
    street = models.CharField(max_length = 200)
    status = models.CharField(max_length = 40)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    sq_ft = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
