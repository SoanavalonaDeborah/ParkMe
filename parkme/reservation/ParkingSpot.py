from .models import ParkingSpot, ParkingPlace

# Créer un nouveau ParkingSpot
spot = ParkingSpot.objects.create(name="Parking A", location="Adresse A")

# Créer 15 places de parking pour ce ParkingSpot
for num in range(1, 16):
    ParkingPlace.objects.create(parking_spot=spot, spot_number=num)
