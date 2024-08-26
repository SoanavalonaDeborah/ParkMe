from celery import shared_task
from django.utils import timezone
from celery.schedules import crontab
from reservation.models import Reservation
from parkme.celery import app


@shared_task
def check_expired_reservations():
    expired_reservations = Reservation.objects.filter(date_de_départ__lt=timezone.now().date(), parking_place__is_available=False)
    for reservation in expired_reservations:
        reservation.parking_place.release()

app.conf.beat_schedule = {
    'check-expired-reservations-every-hour': {
        'task': 'reservations.tasks.check_expired_reservations',
        'schedule': crontab(minute=0, hour='*/1'),  # Toutes les heures
    },
}
