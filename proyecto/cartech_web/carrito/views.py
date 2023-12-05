from django.shortcuts import render, get_object_or_404
from shop.models import Eleccion, Coche, Accesorio, DireccionUsuario
from django.shortcuts import render, redirect 
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CardInformationSerializer  # Make sure to import the serializer
from django.views import View
from .forms import PaymentForm, PedidoForm, DatosClienteForm, DatosEnvioForm
from pedidos.models import Pedido
from django.contrib.auth.models import User
from django.urls import reverse


import stripe

stripe.api_key = 'sk_test_51OJBJcLdnlgk3Y2d9IrdBowToBzxmDRdI2NgP2rTC9tBhTcW2Gebhqllorvp5g1Ru1aSG9Uw1R8k2NN8blJneUyR00Z3eVQBGi'

def home(request):
    return render(request, 'shop/home.html')

# @login_required
def listar_carrito(request):
    usuario = request.user.id
    elecciones = Eleccion.objects.all()
    elecciones = elecciones.filter(usuario_id=usuario, comprado=False)
    precio_total = 0 
    for eleccion in elecciones:
        print(eleccion.comprado)
        precio_total += eleccion.get_precio_total()


    return render(request, 'listar_carrito.html', {'elecciones': elecciones, 'precio_total': precio_total})

def add(request, eleccion_id):
    eleccion = get_object_or_404(Eleccion, id=eleccion_id)

    print(eleccion)
    eleccion.cantidad += 1
    eleccion.save()

    usuario = request.user.id
    elecciones = Eleccion.objects.all()
    elecciones = elecciones.filter(usuario_id=usuario)

    return render(request, 'listar_carrito.html', {'elecciones': elecciones})

def delete(request, eleccion_id):
    eleccion = get_object_or_404(Eleccion, id=eleccion_id)

    print(eleccion)
    eleccion.cantidad -= 1
    if eleccion.cantidad <= 0:
        eleccion.delete()
    else: 
        eleccion.save()

    usuario = request.user.id
    elecciones = Eleccion.objects.all()
    elecciones = elecciones.filter(usuario_id=usuario)
    
    return render(request, 'listar_carrito.html', {'elecciones': elecciones})


def checkout(request):
    usuario = request.user
    elecciones = Eleccion.objects.filter(usuario=usuario, comprado=False)
    detalles_usuario = User.objects.get(username=usuario)

    precio_total = 0
    for eleccion in elecciones:
        precio_total += eleccion.get_precio_total()
    
    print(request.method)
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():

            if form.cleaned_data['metodo_pago'] == 'contra_reembolso':
                pedido = Pedido.objects.create(usuario=usuario)
                pedido.nombre = form.cleaned_data['nombre']
                pedido.apellidos = form.cleaned_data['apellidos']
                pedido.email = form.cleaned_data['email']
                pedido.direccion = form.cleaned_data['direccion']
                pedido.ciudad = form.cleaned_data['ciudad']
                pedido.codigo_postal = form.cleaned_data['codigo_postal']
                pedido.metodo_pago = form.cleaned_data['metodo_pago']
                print(pedido.metodo_pago)
                for eleccion in elecciones:
                    eleccion.comprado = True
                    eleccion.pedido = pedido
                    eleccion.save()
                pedido.save()
                return HttpResponseRedirect(reverse('pedidos:detalle_pedido', args=[pedido.id]))
            else:
                return HttpResponseRedirect('/carrito/make_payment')

            
    else:
        
        # Si es una solicitud GET, inicializa el formulario con los datos de la dirección
        form = PedidoForm(initial={
            'nombre': request.user.first_name,
            'apellidos': detalles_usuario.last_name,
            'email': detalles_usuario.email,
            #'direccion': detalles_usuario.direccion,
            #'ciudad': detalles_usuario.ciudad,
            #'codigo_postal': detalles_usuario.codigo_postal,
        })
        
    return render(request, 'checkout.html', {'elecciones': elecciones, 'form': form, 'precio_total': precio_total })


class PaymentView(View):
    template_name = 'payment_form.html'

    def get(self, request):
        usuario = request.user.id
        elecciones = Eleccion.objects.filter(usuario_id=usuario)
        precio_total = sum(eleccion.get_precio_total() for eleccion in elecciones)

        form = PaymentForm()
        return render(request, self.template_name, {'form': form, 'precio_total': precio_total})

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            usuario = request.user.id
            elecciones = Eleccion.objects.filter(usuario_id=usuario)
            precio_total = sum(eleccion.get_precio_total() for eleccion in elecciones)

            api_data = {
                'card_number': form.cleaned_data['card_number'],
                'expiry_month': form.cleaned_data['expiry_month'],
                'expiry_year': form.cleaned_data['expiry_year'],
                'cvc': form.cleaned_data['cvc'],
            }

            response = self.stripe_card_payment(data_dict=api_data, amount=precio_total)
            
            print("RESPONSE:")
            print(response.get('status'))
            if response.get('status') == status.HTTP_200_OK:
                pedido = Pedido.objects.create(usuario=usuario)
                pedido.nombre = form.cleaned_data['nombre']
                pedido.apellidos = form.cleaned_data['apellidos']
                pedido.email = form.cleaned_data['email']
                pedido.direccion = form.cleaned_data['direccion']
                pedido.ciudad = form.cleaned_data['ciudad']
                pedido.codigo_postal = form.cleaned_data['codigo_postal']
                pedido.metodo_pago = form.cleaned_data['metodo_pago']
                print(pedido.metodo_pago)
                for eleccion in elecciones:
                    eleccion.comprado = True
                    eleccion.pedido = pedido
                    eleccion.save()
                pedido.save()

                return HttpResponseRedirect(reverse('pedidos:detalle_pedido', args=[pedido.id]))
            else:
                return redirect('carrito:listar_carrito')
        else:
            return render(request, self.template_name, {'form': form})

    


    def stripe_card_payment(self, data_dict, amount):
        try:
            card_details = {
                "type": "card",
                "card": {
                    "number": data_dict['card_number'],
                    "exp_month": data_dict['expiry_month'],
                    "exp_year": data_dict['expiry_year'],
                    "cvc": data_dict['cvc'],
                }
            }

            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Multiplica por 100 para convertir a centavos
                currency='eur',
            )

            # Resto del código...

            if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }

        except stripe.error.CardError as e:
            # Since it's a CardError, it should be caught and handled separately
            response = {
                'error': "Your card number is incorrect",
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            response = {
                'error': "An error occurred while processing your payment",
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        except Exception as e:
            # Handle other general exceptions
            response = {
                'error': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }

        return response