from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from reservation.models import Reservation


@receiver(pre_save, sender=Reservation)
def handle_reservation_save(sender, instance, **kwargs):
    # Code pour gérer la mise à jour de la disponibilité des places de parking
    pass

@receiver(post_delete, sender=Reservation)
def handle_reservation_delete(sender, instance, **kwargs):
    # Code pour gérer l'annulation de la réservation et la mise à jour de la disponibilité des places de parking
    pass


@receiver(post_save, sender=Reservation)
def check_reservation_expiry(sender, instance, **kwargs):
    if instance.date_de_départ < timezone.now().date():
        if instance.parking_place:
            instance.parking_place.release()
