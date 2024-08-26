from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from django.core.mail import send_mail
from django.contrib import messages
from reservation.forms import ReservationForm
from reservation.models import Reservation, ParkingPlace
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@csrf_exempt
def save_parkings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            parkings = data.get('parkings', [])
            for parking in parkings:
                parking.objects.create(
                    name=parking['name'],
                    vicinity=parking['vicinity'],
                    latitude=parking['latitude'],
                    longitude=parking['longitude']
                )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def create_reservation(request):
    # Libérer les places de parking des réservations terminées
    reservations = Reservation.objects.all()
    for reservation in reservations:
        reservation.check_and_release_parking_place()

    parking_places = ParkingPlace.objects.filter(is_available=True)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user


            old_reservation = None
            if 'reservation_id' in request.POST:
                reservation_id = request.POST.get('reservation_id')
                old_reservation = Reservation.objects.get(id=reservation_id)

            parking_place_id = request.POST.get('parking_place', None)
            if parking_place_id:
                parking_place = ParkingPlace.objects.get(id=parking_place_id)

                if parking_place.is_available:
                    with transaction.atomic():
                        if old_reservation:
                            old_parking_place = old_reservation.parking_place
                            old_parking_place.is_available = True
                            old_parking_place.save()
                            logger.info(f"Old parking place {old_parking_place.id} released.")

                        parking_place.is_available = False
                        parking_place.save()
                        logger.info(f"Parking place {parking_place.id} reserved.")

                        reservation.parking_place = parking_place
                        reservation.save()
                        logger.info(f"Reservation {reservation.id} created for user {request.user.id}.")


                        # Ajout de l'envoi d'e-mail
                        email = {request.user.email}
                        subject = 'Votre réservation de parking'
                        message = f"Bonjour {request.user.username},\n\nVotre réservation de parking a été effectuée avec succès.\n\nDetails de la réservation :\n{str(reservation)}\n\nMerci et à bientôt !"

                        send_mail(
                            subject, message, 'settings.EMAIL_HOST_USER', email, fail_silently=False
                        )


                        messages.success(request,
                                         'Réservation réussie !Votre mail de confirmation a été bien envoyé! <a href="/reservations/view/">Voir les réservations</a>')
                        return redirect('create_reservation')


                else:
                    logger.warning(f"Parking place {parking_place.id} is no longer available.")
                    messages.error(request, 'Erreur : la place de parking sélectionnée n\'est plus disponible.')
            else:
                messages.error(request,
                               'Erreur lors de la réservation. Veuillez sélectionner un emplacement de parking valide.')
        else:
            messages.error(request, 'Formulaire invalide. Veuillez vérifier les données.')
    else:
        form = ReservationForm()

    return render(request, 'reservation/create_reservation.html', {'form': form, 'parking_places': parking_places})

@login_required
def view_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation/view_reservations.html', {'reservations': reservations})

@login_required
def dashboard(request):
    return render(request, 'auth_app/home.html')

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            old_parking_place = reservation.parking_place
            form.save()
            old_parking_place.is_available = True
            old_parking_place.save()
            logger.info(f"Old parking place {old_parking_place.id} released.")
            messages.success(request, 'Réservation mise à jour avec succès !')
            return redirect('view_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation/edit_reservation.html', {'form': form, 'reservation': reservation})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        parking_place = reservation.parking_place
        parking_place.is_available = True
        parking_place.save()
        logger.info(f"Parking place {parking_place.id} released.")
        reservation.delete()
        messages.success(request, 'Réservation annulée avec succès !')
        return redirect('view_reservations')
    return render(request, 'reservation/cancel_reservation.html', {'reservation': reservation})
