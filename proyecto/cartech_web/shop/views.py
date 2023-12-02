from django.shortcuts import render, get_object_or_404
from .models import  Coche, Accesorio, Eleccion
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'shop/home.html')

@login_required
def cars_list(request):
    combustible = request.GET.get('combustible', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    cars = Coche.objects.all()
    if combustible:
        cars = cars.filter(combustible=combustible)
    if precio_maximo:
        cars = cars.filter(precio_inicial__lte=precio_maximo)
    if tipo_conduccion:
        cars = cars.filter(conduccion=tipo_conduccion)
    if consumo:
        cars = cars.filter(consumo__lte = consumo)
    if caballos:
        cars = cars.filter(caballos__lte =caballos)
    context = {
        'cars': cars,
        'combustible': combustible,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'shop/cars/listar_coches.html', context)

@login_required
def car_detail(request, id):
    car = get_object_or_404(Coche, id=id)
    accesorios_disponibles = Accesorio.objects.all()

    if request.method == 'POST':
        
        if 'confirmar_eleccion' in request.POST:
            accesorios_seleccionados_ids = request.POST.getlist('accesorios_seleccionados', [])
            accesorios_seleccionados = Accesorio.objects.filter(id__in=accesorios_seleccionados_ids)

        elif 'comprar' in request.POST:
            accesorios_comprar_ids = request.POST.getlist('accesorios_comprar', [])
            accesorios_comprar = Accesorio.objects.filter(id__in=accesorios_comprar_ids)
            eleccion = Eleccion(coche=car, usuario = request.user)
            eleccion.save()
            eleccion.accesorios.set(accesorios_comprar)
            print('accesorios', eleccion.coche)
            print('accesorios', eleccion.accesorios.all())
            return HttpResponseRedirect('/')

    else:
        accesorios_seleccionados = []

    precio_total = car.precio_inicial + sum(accesorio.precio for accesorio in accesorios_seleccionados)
    context = {
        'car': car,
        'accesorios_disponibles': accesorios_disponibles,
        'accesorios_seleccionados': accesorios_seleccionados,
        'precio_total': precio_total,
    }
    return render(request, 'shop/cars/detail.html', context)
