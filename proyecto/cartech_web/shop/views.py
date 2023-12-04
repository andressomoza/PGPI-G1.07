from django.shortcuts import render, get_object_or_404
from .models import  Coche, Accesorio, Eleccion
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Count
from .forms import CocheForm, AccesorioForm
from django.contrib.auth.decorators import user_passes_test
from cartech_web.views import is_admin

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about/about.html')

def contact(request):
    return render(request, 'contact/contact.html')

def selector(request):
    return render(request,'coches/selector.html')

@user_passes_test(is_admin)
def crear_accesorio(request):
    if request.method == 'POST':
        form = AccesorioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accesorios/list')   # Puedes definir esta vista
    else:
        form = AccesorioForm()

    return render(request, 'accesorios/crear_accesorio.html', {'form': form})

@user_passes_test(is_admin)
def editar_accesorio(request, id):
    accesorio = get_object_or_404(Accesorio, id=id)

    if request.method == 'POST':
        form = AccesorioForm(request.POST, request.FILES, instance=accesorio)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accesorios/list')  # Ajusta la redirección según tus necesidades
    else:
        form = AccesorioForm(instance=accesorio)

    return render(request, 'accesorios/editar_accesorio.html', {'form': form, 'accesorio': accesorio})

@user_passes_test(is_admin)
def borrar_accesorio(request, id):
    accesorio = get_object_or_404(Accesorio, id=id)

    if request.method == 'POST':
        accesorio.delete()
        return HttpResponseRedirect('/list/accesorios')  

    return render(request, 'accesorios/borrar_accesorio.html', {'accesorio': accesorio})

def listado_accesorios(request):
    con_stock = request.GET.get('con_stock', False)
    nombre = request.GET.get('nombre', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    accesorios = Accesorio.objects.all()
    if con_stock:
        accesorios = accesorios.filter(stock__gt=0)
    if nombre:
        accesorios = accesorios.filter(nombre__icontains=nombre)
    if precio_maximo:
        accesorios = accesorios.filter(precio__lte = precio_maximo)

    context = {
        'accesorios': accesorios,
        'nombre': nombre,
        'con_stock': con_stock,
        'precio_maximo': precio_maximo,

    }

    return render(request, 'accesorios/listar_accesorios.html', context)

def detalles_accesorio(request, id):
    accesorio = get_object_or_404(Accesorio, id=id)
        
    context = {
        'accesorio': accesorio,

    }
    return render(request, 'accesorios/detalle.html', context)

@user_passes_test(is_admin)
def crear_coche(request):
    if request.method == 'POST':
        form = CocheForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/coches/list') 
    else:
        form = CocheForm()

    return render(request, 'coches/crear_coche.html', {'form': form})

@user_passes_test(is_admin)
def editar_coche(request, id):
    coche = get_object_or_404(Coche, id=id)

    if request.method == 'POST':
        form = CocheForm(request.POST, request.FILES, instance=coche)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/coches/list') # Ajusta la redirección según tus necesidades
    else:
        form = CocheForm(instance=coche)

    return render(request, 'coches/editar_coche.html', {'form': form, 'coche': coche})

@user_passes_test(is_admin)
def borrar_coche(request, id):
    coche = get_object_or_404(Coche, id=id)

    if request.method == 'POST':
        coche.delete()
        return HttpResponseRedirect('/coches/list')  # Ajusta la redirección según tus necesidades

    return render(request, 'coches/borrar_coche.html', {'coche': coche})

def listado_coches(request):
    con_stock = request.GET.get('con_stock', False)
    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    combustible = request.GET.get('combustible', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    coches = Coche.objects.all()
    if con_stock:
        coches = coches.filter(stock__gt=0)
    if marca:
        coches = coches.filter(marca__icontains=marca)
    if modelo:
        coches = coches.filter(modelo__icontains=modelo)
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

    usuario = request.user.id
    elecciones = Eleccion.objects.all()
    elecciones = elecciones.filter(usuario_id=usuario).values()
        
    context = {
        'coches': coches,
        'marca': marca,
        'modelo': modelo,
        'con_stock': con_stock,
        'combustible': combustible,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
        'elecciones': elecciones
    }

    return render(request, 'coches/listar_coches.html', context)

def listado_electricos(request):
    con_stock = request.GET.get('con_stock', False)
    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    coches = Coche.objects.filter(combustible = 'electrico')
    if con_stock:
        coches = coches.filter(stock__gt=0)
    if marca:
        coches = coches.filter(marca__icontains=marca)
    if modelo:
        coches = coches.filter(modelo__icontains=modelo)
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
        'marca': marca,
        'con_stock': con_stock,
        'modelo': modelo,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'coches/listar_electricos.html', context)

def listado_hibridos(request):
    con_stock = request.GET.get('con_stock', False)
    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    coches = Coche.objects.filter(combustible = 'hibrido')
    if con_stock:
        coches = coches.filter(stock__gt=0)
    if marca:
        coches = coches.filter(marca__icontains=marca)
    if modelo:
        coches = coches.filter(modelo__icontains=modelo)
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
        'marca': marca,
        'con_stock': con_stock,
        'modelo': modelo,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'coches/listar_hibridos.html', context)

def listado_combustible(request):
    con_stock = request.GET.get('con_stock', False)
    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    coches = Coche.objects.filter(combustible__in=['gasolina', 'diesel'])
    combustible = request.GET.get('combustible', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    if con_stock:
        coches = coches.filter(stock__gt=0)
    if marca:
        coches = coches.filter(marca__icontains=marca)
    if modelo:
        coches = coches.filter(modelo__icontains=modelo)
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
        'marca': marca,
        'con_stock': con_stock,
        'modelo': modelo,
        'combustible':combustible,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'coches/listar_combustible.html', context)

def detalles_coche(request, id):
    coche = get_object_or_404(Coche, id=id)
    accesorios_disponibles = Accesorio.objects.all()
    alerta = None
    accesorios_seleccionados = []
    cantidad= 1

    if request.method == 'POST':
        
        if 'confirmar_eleccion' in request.POST:
            accesorios_seleccionados_ids = request.POST.getlist('accesorios_seleccionados', [])
            accesorios_seleccionados = Accesorio.objects.filter(id__in=accesorios_seleccionados_ids)
            
        elif 'comprar' in request.POST:
            accesorios_comprar_ids = request.POST.getlist('accesorios_comprar', [])
            accesorios_comprar = Accesorio.objects.filter(id__in=accesorios_comprar_ids)
            cantidad = int(request.POST.get('cantidad', 1))
            eleccion_existente = Eleccion.objects.filter(
                coche=coche,
                usuario=request.user,
                accesorios__in=accesorios_comprar,
            ).annotate(accesorios_count=Count('accesorios')).filter(accesorios_count=len(accesorios_comprar)).first()
            
            if eleccion_existente:
                alerta = "Ya existe una elección con los mismos accesorios, añada mas desde el carrito."
            else:
                eleccion = Eleccion(coche=coche, usuario = request.user, cantidad = cantidad)
                eleccion.save()
                eleccion.accesorios.set(accesorios_comprar)
                return HttpResponseRedirect('/')
        

    precio_total = coche.precio_inicial + sum(accesorio.precio for accesorio in accesorios_seleccionados)
    context = {
        'coche': coche,
        'alerta':alerta,
        'cantidad':cantidad,
        'accesorios_disponibles': accesorios_disponibles,
        'accesorios_seleccionados': accesorios_seleccionados,
        'precio_total': precio_total,
    }
    return render(request, 'coches/detail.html', context)
