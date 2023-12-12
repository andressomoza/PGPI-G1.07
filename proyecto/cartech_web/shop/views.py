from django.shortcuts import render, get_object_or_404
from .models import  Coche, Accesorio, Eleccion
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Count
from .forms import CocheForm, AccesorioForm
from django.contrib.auth.decorators import user_passes_test
from cartech_web.views import is_admin
from django.db.models import Sum, Count, F,  ExpressionWrapper, DecimalField,fields
from django.db import models
from pedidos.models import Pedido

def home(request):
    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
    return render(request,'home.html', {'elecciones': elecciones})

def about(request):
    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
    return render(request, 'about/about.html', {'elecciones': elecciones})

def contact(request):
    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
    return render(request, 'contact/contact.html', {'elecciones': elecciones})

def selector(request):
    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
    return render(request,'coches/selector.html', {'elecciones': elecciones})

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
    elecciones = elecciones.filter(usuario_id=usuario, comprado=False)
        
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

    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)

    context = {
        'coches': coches,
        'marca': marca,
        'con_stock': con_stock,
        'modelo': modelo,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
        'elecciones': elecciones
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

    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)

    context = {
        'coches': coches,
        'marca': marca,
        'con_stock': con_stock,
        'modelo': modelo,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
        'elecciones': elecciones
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

    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
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
        'elecciones': elecciones
    }

    return render(request, 'coches/listar_combustible.html', context)

def detalles_coche(request, id):
    coche = get_object_or_404(Coche, id=id)
    elecciones_coche = Eleccion.objects.filter(coche = coche)
    opiniones = []
    for eleccion in elecciones_coche:
        opiniones.append(eleccion.opinion)
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
                return HttpResponseRedirect('/carrito/')
        elif 'ya' in request.POST:
            accesorios_comprar_ids = request.POST.getlist('accesorios_comprar', [])
            accesorios_comprar = Accesorio.objects.filter(id__in=accesorios_comprar_ids)
            cantidad = int(request.POST.get('cantidad', 1))
            eleccion = Eleccion(coche=coche, usuario = request.user, cantidad = cantidad)
            eleccion.save()
            eleccion.accesorios.set(accesorios_comprar)
            return HttpResponseRedirect('/carrito/checkout')

    precio_total = coche.precio_inicial + sum(accesorio.precio for accesorio in accesorios_seleccionados)
    context = {
        'coche': coche,
        'alerta':alerta,
        'cantidad':cantidad,
        'opiniones':opiniones,
        'accesorios_disponibles': accesorios_disponibles,
        'accesorios_seleccionados': accesorios_seleccionados,
        'precio_total': precio_total,
    }
    return render(request, 'coches/detail.html', context)

@user_passes_test(is_admin)
def estadisticas_base(request):
    return render(request, 'estadisticas/base_estadisticas.html')

@user_passes_test(is_admin)
def estadisticas_coches(request):
    # Cantidad de coches vendidos
    coches_vendidos = Eleccion.objects.filter(comprado=True).aggregate(total_coches_vendidos=Sum('cantidad'))['total_coches_vendidos'] or 0


    # Coches más vendidos
    coches_mas_vendidos_ids = Eleccion.objects.values('coche__id').annotate(cantidad_vendida=Count('coche__id')).order_by('-cantidad_vendida')[:3]
    coches_mas_vendidos = Coche.objects.filter(id__in=[coche_stat['coche__id'] for coche_stat in coches_mas_vendidos_ids])
    cant_coches_vendidos={}
    for coche in coches_mas_vendidos:
        elecciones = Eleccion.objects.filter(coche = coche).all()
        num = 0
        for eleccion in elecciones: 
            num += eleccion.cantidad
        cant_coches_vendidos[coche]=num

    # Dinero total recibido (solo por el coche, sin contar accesorios)
    dinero_total_recibido_por_coches = Eleccion.objects.filter(comprado=True).aggregate(
        total_dinero=Sum(F('cantidad') * F('coche__precio_inicial'), output_field=models.IntegerField())
        )['total_dinero'] or 0


    # Combustible más vendido
    combustible_mas_vendido = Eleccion.objects.filter(comprado=True).values('coche__combustible').annotate(cantidad_vendida=Count('coche__combustible')).order_by('-cantidad_vendida').first()


    # Datos para el gráfico de pastel - Tipos de Combustible
    tipos_combustible = Coche.Combustible.choices
    labels_combustible = [choice[1] for choice in tipos_combustible]
    data_combustible = [Eleccion.objects.filter(comprado=True, coche__combustible=choice[0]).count() for choice in tipos_combustible]

    # Datos para el gráfico de pastel - Tipo de Conducción
    tipos_conduccion = Coche.Conduccion.choices
    labels_conduccion = [choice[1] for choice in tipos_conduccion]
    data_conduccion = [Eleccion.objects.filter(comprado=True, coche__conduccion=choice[0]).count() for choice in tipos_conduccion]

    # Cantidad total de pedidos
    elecciones = Eleccion.objects.filter(comprado=True) 
    pedidos = set()
    for eleccion in elecciones:
        pedido = Pedido.objects.filter(elecciones__in=[eleccion])
        pedidos.add(pedido)
    num_pedidos = len(pedidos)
    # Dinero total recaudado 
    dinero_total_exp = ExpressionWrapper(
        (F('coche__precio_inicial')) * F('cantidad'),
        output_field=DecimalField(),
    )
    dinero_total_recaudado = Eleccion.objects.filter(comprado=True).aggregate(total_recaudado=Sum(dinero_total_exp))['total_recaudado'] or 0


    context = {
        'cant_coches_vendidos': cant_coches_vendidos,
        'coches_vendidos': coches_vendidos,
        'dinero_total_recibido_por_coches': dinero_total_recibido_por_coches,
        'combustible_mas_vendido': combustible_mas_vendido,
        'labels_combustible': labels_combustible,
        'data_combustible': data_combustible,
        'labels_conduccion': labels_conduccion,
        'data_conduccion': data_conduccion,
        'num_pedidos': num_pedidos,
        'dinero_total_recaudado': dinero_total_recaudado,
    }

    return render(request, 'estadisticas/estadisticas_coches.html', context)

@user_passes_test(is_admin)
def estadisticas_accesorios(request):
    
    numero_accesorios_vendidos = Eleccion.objects.filter(comprado=True).aggregate(total_accesorios_vendidos=Sum('cantidad'))['total_accesorios_vendidos'] or 0
    
    dinero_por_accesorio = ExpressionWrapper(
        F('accesorios__precio') * F('cantidad'),
        output_field=fields.DecimalField(),
    )

    # Calcular el dinero total ganado con accesorios sumando la expresión anterior
    dinero_ganado_accesorios = Eleccion.objects.filter(comprado=True).aggregate(
        total_dinero_accesorios=Sum(dinero_por_accesorio)
    )['total_dinero_accesorios'] or 0
    
    
    accesorios_mas_vendidos = Accesorio.objects.annotate(cantidad_vendida=Sum('elecciones__cantidad')).order_by('-cantidad_vendida')[:3]

    cant_accesorios_vendidos={}
    for accesorio in accesorios_mas_vendidos:
        elecciones = Eleccion.objects.filter(accesorios__in=[accesorio]).all()

        num = sum(eleccion.cantidad for eleccion in elecciones)
    
        cant_accesorios_vendidos[accesorio]=num
        
    context = {
        'numero_accesorios_vendidos': numero_accesorios_vendidos,
        'dinero_ganado_accesorios': dinero_ganado_accesorios,
        'cant_accesorios_vendidos': cant_accesorios_vendidos,
    }

    print(context)
    return render(request, 'estadisticas/estadisticas_accesorios.html',context)