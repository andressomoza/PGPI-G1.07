from django.shortcuts import render, get_object_or_404
from .models import  Coche, Accesorio, Eleccion
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count


def home(request):
    return render(request,'shop/home.html')

def selector(request):
    return render(request,'shop/coches/selector.html')

@login_required
def listado_coches(request):
    combustible = request.GET.get('combustible', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    coches = Coche.objects.all()
    if combustible:
        coches = coches.filter(combustible=combustible)
    if precio_maximo:
        coches = coches.filter(precio_inicial__lte=precio_maximo)
    if tipo_conduccion:
        coches = coches.filter(conduccion=tipo_conduccion)
    if consumo:
        coches = coches.filter(consumo__lte = consumo)
    if caballos:
        coches = coches.filter(caballos__lte =caballos)
    context = {
        'coches': coches,
        'combustible': combustible,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'shop/coches/listar_coches.html', context)

@login_required
def listado_electricos(request):
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    coches = Coche.objects.filter(combustible = 'electrico')
    if precio_maximo:
        coches = coches.filter(precio_inicial__lte=precio_maximo)
    if tipo_conduccion:
        coches = coches.filter(conduccion=tipo_conduccion)
    if consumo:
        coches = coches.filter(consumo__lte = consumo)
    if caballos:
        coches = coches.filter(caballos__lte =caballos)
    context = {
        'coches': coches,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'shop/coches/listar_electricos.html', context)

@login_required
def listado_hibridos(request):
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    coches = Coche.objects.filter(combustible = 'hibrido')
    if precio_maximo:
        coches = coches.filter(precio_inicial__lte=precio_maximo)
    if tipo_conduccion:
        coches = coches.filter(conduccion=tipo_conduccion)
    if consumo:
        coches = coches.filter(consumo__lte = consumo)
    if caballos:
        coches = coches.filter(caballos__lte =caballos)
    context = {
        'coches': coches,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'shop/coches/listar_hibridos.html', context)

@login_required
def listado_combustible(request):
    coches = Coche.objects.filter(combustible__in=['gasolina', 'diesel'])
    combustible = request.GET.get('combustible', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    if combustible:
        coches = coches.filter(combustible=combustible)
    if precio_maximo:
        coches = coches.filter(precio_inicial__lte=precio_maximo)
    if tipo_conduccion:
        coches = coches.filter(conduccion=tipo_conduccion)
    if consumo:
        coches = coches.filter(consumo__lte = consumo)
    if caballos:
        coches = coches.filter(caballos__lte =caballos)
    context = {
        'coches': coches,
        'combustible':combustible,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'shop/coches/listar_combustible.html', context)

@login_required
def detalles(request, id):
    coche = get_object_or_404(Coche, id=id)
    accesorios_disponibles = Accesorio.objects.all()
    alerta = None
    accesorios_seleccionados = []

    if request.method == 'POST':
        
        if 'confirmar_eleccion' in request.POST:
            accesorios_seleccionados_ids = request.POST.getlist('accesorios_seleccionados', [])
            accesorios_seleccionados = Accesorio.objects.filter(id__in=accesorios_seleccionados_ids)
            
        elif 'comprar' in request.POST:
            accesorios_comprar_ids = request.POST.getlist('accesorios_comprar', [])
            accesorios_comprar = Accesorio.objects.filter(id__in=accesorios_comprar_ids)
            eleccion_existente = Eleccion.objects.filter(
                coche=coche,
                usuario=request.user,
                accesorios__in=accesorios_comprar,
            ).annotate(accesorios_count=Count('accesorios')).filter(accesorios_count=len(accesorios_comprar)).first()
            
            if eleccion_existente:
                alerta = "Ya existe una elección con los mismos accesorios, añada mas desde el carrito."
            else:
                eleccion = Eleccion(coche=coche, usuario = request.user)
                eleccion.save()
                eleccion.accesorios.set(accesorios_comprar)
                return HttpResponseRedirect('/')
        

    precio_total = coche.precio_inicial + sum(accesorio.precio for accesorio in accesorios_seleccionados)
    context = {
        'coche': coche,
        'alerta':alerta,
        'accesorios_disponibles': accesorios_disponibles,
        'accesorios_seleccionados': accesorios_seleccionados,
        'precio_total': precio_total,
    }
    return render(request, 'shop/coches/detail.html', context)
