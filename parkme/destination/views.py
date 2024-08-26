from django.shortcuts import render

def acceuil(request):
    return render(request, 'destination/acceuil.html')

def apropos(request):
    return render(request, 'destination/apropos.html')

def apropos2(request):
    return render(request, 'destination/apropos2.html')

def tana(request):
    return render(request, 'destination/tana.html')

def antsirabe(request):
    return render(request, 'destination/antsirabe.html')

def fianarantsoa(request):
    return render(request, 'destination/fianarantsoa.html')

def mahajanga(request):
    return render(request, 'destination/mahajanga.html')

def toamasina(request):
    return render(request, 'destination/toamasina.html')

def toliara(request):
    return render(request, 'destination/toliara.html')

# Create your views here.
