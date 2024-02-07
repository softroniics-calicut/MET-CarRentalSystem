from django.contrib import admin
from .models import  customusers, Car, Booking
from django.contrib.auth.models import Group
# Register your models here.

class customusersAdmin(admin.ModelAdmin):  
    list_display = ('username', 'email', 'user_type', 'address', 'phone', 'location')
    search_fields = ('username', 'email', 'company_name')
    list_filter = ('user_type', 'location')
    readonly_fields = ('first_name','last_name','username','password', 'email', 'user_type', 'address', 'phone', 'location','company_name' ) 
    list_per_page = 10
    def get_fields(self, request, obj=None):
        # Exclude 'company_name' field for 'user' type and 'driving_licence' for 'company' type
        if obj and obj.user_type == 'user':
            return ('first_name','last_name','username', 'email', 'user_type', 'address', 'phone', 'location', 'driving_licence')
        elif obj and obj.user_type == 'company':
            return ('first_name','last_name','username', 'email', 'user_type', 'address', 'phone', 'location','company_name')

        return super().get_fields(request, obj)

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_id', 'car_model', 'price', 'status')
    search_fields = ('name', 'car_model', 'company_id__company_name')
    readonly_fields = ('status','name','car_model', 'price', 'details','company_id') 
    list_per_page = 20

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car','company_name', 'no_of_days', 'Total_cost', 'booking_date', 'status')
    search_fields = ('user__username', 'car__name')
    list_filter = ('status',)
    readonly_fields = ('user', 'car', 'starting_day', 'no_of_days', 'Total_cost', 'booking_date', 'status', 'Rating','review') 
    list_per_page = 20

    def company_name(self, obj):
        return obj.car.company_id.company_name if obj.car and obj.car.company_id else ''

    company_name.short_description = 'Company Name'

admin.site.register(customusers, customusersAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)

admin.site.unregister(Group)
admin.site.site_header = 'Royal Cars'