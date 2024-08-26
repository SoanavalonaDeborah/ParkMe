from django import forms
from .models import Reservation, ParkingPlace
from django.core.exceptions import ValidationError
from django.db.models import Q


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['parking_place', 'type_de_véhicule', 'numéro_de_plaque', 'date_d_arriver', 'date_de_départ',
                  'heure_d_arriver', 'heure_de_départ', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parking_place'].queryset = ParkingPlace.objects.filter(is_available=True)

        # Personnalisation du champ email
        self.fields['email'].widget.attrs.update({'class': 'email-input-class'})  # Ajoutez une classe CSS si nécessaire

    def clean(self):
        cleaned_data = super().clean()
        parking_place = cleaned_data.get('parking_place')
        heure_d_arriver = cleaned_data.get('heure_d_arriver')
        heure_de_départ = cleaned_data.get('heure_de_départ')

        # Check if the reservation being edited
        if self.instance.pk:
            existing_reservations = Reservation.objects.filter(
                Q(parking_place=parking_place),
                Q(heure_d_arriver__lt=heure_de_départ, heure_de_départ__gt=heure_d_arriver) |
                Q(heure_d_arriver__gte=heure_de_départ, heure_de_départ__lte=heure_d_arriver),
                Q(pk=self.instance.pk)  # Exclude current reservation
            )
        else:
            existing_reservations = Reservation.objects.filter(
                Q(parking_place=parking_place),
                Q(heure_d_arriver__lt=heure_de_départ, heure_de_départ__gt=heure_d_arriver) |
                Q(heure_d_arriver__gte=heure_de_départ, heure_de_départ__lte=heure_d_arriver)
            )

        if existing_reservations.exists():
            raise ValidationError("Ce créneau horaire est déjà réservé pour cette place de parking.")

        return cleaned_data

