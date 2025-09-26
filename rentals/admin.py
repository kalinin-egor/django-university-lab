from django.contrib import admin

from .models import Car, Client, ExtraService, Rental


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'vin', 'color', 'daily_rental_price')
    list_filter = ('brand', 'year', 'color')
    search_fields = ('brand', 'model', 'vin')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'driver_license_number', 'phone_number', 'email')
    search_fields = ('full_name', 'driver_license_number', 'email')


@admin.register(ExtraService)
class ExtraServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'client', 'start_date', 'end_date', 'total_cost', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('car__brand', 'car__model', 'client__full_name')
    filter_horizontal = ('extra_services',)
