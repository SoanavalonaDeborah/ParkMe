from django.contrib import admin
from django.urls import path
from destination.views import acceuil, tana, antsirabe, fianarantsoa, mahajanga, toamasina, toliara, apropos, apropos2
from auth_app.views import inscription, connexion, deconnexion, home
from reservation.views import save_parkings, create_reservation, view_reservations, edit_reservation, cancel_reservation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', acceuil, name='acceuil'),
    path('inscription/',inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('home/', home, name='home'),
    path('deconnexion', deconnexion, name='deconnexion'),
    path('save_parkings/', save_parkings, name='save_parkings'),
    path('tana/', tana, name='tana'),
    path('antsirabe/', antsirabe, name='antsirabe'),
    path('fianarantsoa/', fianarantsoa, name='fianarantsoa'),
    path('mahajanga/', mahajanga, name='mahajanga'),
    path('toamasina/', toamasina, name='toamasina'),
    path('toliara/', toliara, name='toliara'),
    path('reservations/create/', create_reservation, name='create_reservation'),
    path('reservations/view/', view_reservations, name='view_reservations'),
    path('reservations/edit/<int:reservation_id>/', edit_reservation, name='edit_reservation'),
    path('reservations/cancel/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path('apropos/', apropos, name='apropos'),
    path('apropos2/', apropos2, name='apropos2'),
]