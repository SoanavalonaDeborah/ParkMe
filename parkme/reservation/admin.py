from django.contrib import admin
from .models import ParkingSpot, ParkingPlace, Reservation


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(ParkingPlace)
class ParkingPlaceAdmin(admin.ModelAdmin):
    list_display = ('parking_spot', 'spot_number', 'is_available')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'parking_place', 'type_de_véhicule', 'numéro_de_plaque', 'date_d_arriver', 'date_de_départ', 'heure_d_arriver', 'heure_de_départ')
