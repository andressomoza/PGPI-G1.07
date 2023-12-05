from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Pedido
from shop.models import Eleccion
from django.contrib.auth.decorators import user_passes_test
from cartech_web.views import is_admin
from django.http import HttpResponseRedirect
from .forms import PedidoForm

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

@user_passes_test(is_admin)
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pedidos/', id)   
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'editar_pedido.html', {'form': form, 'pedido': pedido})

@user_passes_test(is_admin)
def borrar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == 'POST':
        pedido.delete()
        return HttpResponseRedirect('/pedidos/')  

    return render(request, 'borrar_pedido.html', {'pedido': pedido})

@user_passes_test(is_admin)
def listar_pedidos(request):
    status = request.GET.get('status', '')
    
    pedidos = Pedido.objects.all()
    if status:
        pedidos = pedidos.filter(status=status)
    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)

    context = {
        'pedidos': pedidos,
        'status': status,
        'elecciones': elecciones
    }
    return render(request, 'listar_pedidos.html', context)

def buscar_pedido(request):
    if request.method == 'POST':
        id_pedido = request.POST.get('id_pedido')
        if id_pedido:
            pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
            elecciones = Eleccion.objects.filter(pedido = pedido).all()
            precio_total = 0
            for eleccion in elecciones:
                precio_total+= eleccion.get_precio_total()
            
            usuario = request.user.id
            elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
            context = {
                'pedido': pedido,
                'elecciones': elecciones,
                'precio_total':precio_total,
                'elecciones': elecciones
            }
            return render(request, 'detalle_pedido.html', context)
        else:
            return HttpResponse("Por favor, proporciona un ID de pedido válido.")
    else:
        return render(request, 'buscar_pedido.html')

def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario = request.user)

    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
    context = {
        'pedidos': pedidos,
        'elecciones': elecciones
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
        precio_total+= eleccion.get_precio_total()
    context = {
        'pedido': pedido,
        'elecciones': elecciones,
        'precio_total':precio_total,

    }
    return render(request, 'detalle_pedido.html', context)
