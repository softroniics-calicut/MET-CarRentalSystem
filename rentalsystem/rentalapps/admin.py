from django.contrib import admin
from .models import  customusers
from .models import  Car
from .models import  Booking
# Register your models here.

admin.site.register(customusers)
admin.site.register(Booking)
admin.site.register(Car)
