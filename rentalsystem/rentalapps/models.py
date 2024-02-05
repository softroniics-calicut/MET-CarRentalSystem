from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date
# Create your models here.

class customusers(AbstractUser):
    address = models.CharField(max_length=225, null=True)
    user_type = models.CharField(max_length=20)
    phone = models.IntegerField(null=True)
    location = models.CharField(max_length=255,null=True)
    company_name = models.CharField(max_length=225,null=True, blank=True)
    driving_licence = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.username



class Car(models.Model):
    company_id = models.ForeignKey(customusers, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)
    image = models.FileField()
    car_model = models.CharField(max_length=225,null=True)
    details = models.TextField(max_length=255,null=True)
    price = models.IntegerField(null=True)
    status = models.CharField(max_length=20,default="Available", null=True,blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(customusers, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    starting_day = models.DateField()
    # ending_day = models.DateField()
    no_of_days = models.IntegerField()
    Total_cost = models.IntegerField(null=True)
    booking_date = models.DateField(default=timezone.now)
    status = models.CharField(default='pending',max_length=255)
    review = models.CharField(max_length=255,null=True)
    Rating = models.IntegerField(null=True)




