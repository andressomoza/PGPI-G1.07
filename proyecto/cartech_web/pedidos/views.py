from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Pedido
from shop.models import Eleccion


def crear_pedido(request):
    '''
    if request.method == 'POST':
        form = IncidenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_incidencias')  # Puedes definir esta vista
    else:
        form = IncidenciaForm()

    return render(request, 'incidencias/crear_incidencia.html', {'form': form})
    '''
    return render(request, 'checkout.html')


def listar_pedidos(request):
    status = request.GET.get('status', '')
    
    pedidos = Pedido.objects.all()
    if status:
        pedidos = pedidos.filter(status=status)

    context = {
        'pedidos': pedidos,
        'status': status,
    }
    return render(request, 'listar_pedidos.html', context)

def buscar_pedido(request):
    if request.method == 'POST':
        id_pedido = request.POST.get('id_pedido')
        if id_pedido:
            pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
            return render(request, 'detalles_pedido.html', {'pedido': pedido})
        else:
            return HttpResponse("Por favor, proporciona un ID de pedido válido.")
    else:
        return render(request, 'buscar_pedido.html')

def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario = request.user)

    context = {
        'pedidos': pedidos,
    }

    return render(request, 'mis_pedidos.html', context)

def detalle_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    print("pedido: ")
    print(pedido.id)
    elecciones = Eleccion.objects.filter(pedido=pedido.id)
    print("HOLA")
    for eleccion in elecciones:
        print(eleccion.pedido.id)

    precio_total = 0
    for eleccion in elecciones:
        precio_total += eleccion.get_precio_total()
        
    return render(request, 'detalle_pedido.html', {'elecciones': elecciones, 'precio_total': precio_total, 'pedido': pedido})
