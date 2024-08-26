from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class ParkingSpot(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ParkingPlace(models.Model):
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    spot_number = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.parking_spot.name} - Place {self.spot_number}"

    def reserve(self):
        self.is_available = False
        self.save()

    def release(self):
        self.is_available = True
        self.save()
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, default=1)
    type_de_véhicule = models.CharField(max_length=20, default='voiture')
    numéro_de_plaque = models.CharField(max_length=20, default='0000 abc')
    date_d_arriver = models.DateField(default=timezone.now)
    date_de_départ = models.DateField(default=timezone.now)
    heure_d_arriver = models.DateTimeField(default=timezone.now().replace(hour=8, minute=0))
    heure_de_départ = models.DateTimeField(default=timezone.now().replace(hour=9, minute=0))
    parking_place = models.ForeignKey(ParkingPlace, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return f"Reservation #{self.id} - {self.user.username}"

    def is_cancelled(self):
        return self.date_de_départ < self.date_d_arriver

    def duration(self):
        return (self.date_de_départ - self.date_d_arriver).days + 1

    def check_and_release_parking_place(self):
        now = timezone.now()
        if self.heure_de_départ < now and self.parking_place and not self.parking_place.is_available:
            self.parking_place.release()

