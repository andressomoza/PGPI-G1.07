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
from user.models import User
from django.urls import reverse
import smtplib
from email.mime.text import MIMEText


import stripe

stripe.api_key = 'sk_test_51OJBJcLdnlgk3Y2d9IrdBowToBzxmDRdI2NgP2rTC9tBhTcW2Gebhqllorvp5g1Ru1aSG9Uw1R8k2NN8blJneUyR00Z3eVQBGi'

def home(request):
    return render(request, 'shop/home.html')


def send_email(reci, cuerpo):
    subject = "¡Pedido realizado!"
    body = cuerpo
    sender = "cartechw@gmail.com"
    recipient = reci
    password = "wafo rwpp osty blpg"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipient)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipient, msg.as_string())
    print("Message sent!")

def preparar_cuerpo_email(pedido, elecciones, precio_total):
    cuerpo = ""
    str1 = "¡Su pedido con ID " + str(pedido.id) + " ha sido recibido!\n"
    str2 = "Los datos del pedido son: " + pedido.nombre + " " + pedido.apellidos + " en la dirección: " + pedido.direccion + ", " + pedido.ciudad + " (" + str(pedido.codigo_postal) + ")\n"
    str3 = "El contenido del pedido es el siguiente:\n"
    cuerpo = cuerpo + str1 + str2 + str3
    for eleccion in elecciones:
        str4 = " - " + str(eleccion.cantidad) + "x Marca: " + eleccion.coche.marca + " " + eleccion.coche.modelo + ". Combustible: " + eleccion.coche.combustible + ". Conducción: " + eleccion.coche.conduccion + ". Consumo:" + str(eleccion.coche.consumo) + ". Caballos: " + str(eleccion.coche.caballos) + ". Precio inicial: " + str(eleccion.coche.precio_inicial) + "€. "
        str5 = "Con los siguientes accesorios:"

        for accesorio in eleccion.accesorios.all():
            str6 = " " + accesorio.nombre + ", cuyo precio es " + str(accesorio.precio) + "€. "
            str5 = str5 + str6
        str4 = str4 + str5
        cuerpo = cuerpo + str4
    cuerpo = cuerpo + "\nPrecio total: " + str(precio_total) + "€."
    return cuerpo  


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
    if eleccion.coche.stock > eleccion.cantidad:
        eleccion.cantidad += 1
        eleccion.save()

    usuario = request.user.id
    elecciones = Eleccion.objects.all()
    elecciones = elecciones.filter(usuario_id=usuario)

    return redirect('carrito:listar_carrito')

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
    
    return redirect('carrito:listar_carrito')

def limpiar(request, eleccion_id):
    eleccion = get_object_or_404(Eleccion, id=eleccion_id)
    eleccion.delete()

    usuario = request.user.id
    elecciones = Eleccion.objects.all()
    elecciones = elecciones.filter(usuario_id=usuario)
    return redirect('carrito:listar_carrito')

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
                    coche = Coche.objects.filter(id=eleccion.coche.id)
                    coche = coche.get()
                    coche.stock = coche.stock - eleccion.cantidad
                    coche.save()
                    eleccion.save()
                pedido.save()
                
                cuerpo = preparar_cuerpo_email(pedido, elecciones, precio_total)
                send_email('andressomozasierra@gmail.com', cuerpo)
                return HttpResponseRedirect(reverse('pedidos:detalle_pedido', args=[pedido.id]))
            else:
                return HttpResponseRedirect(reverse('carrito:payment_view') + f"?nombre={form.cleaned_data['nombre']}&apellidos={form.cleaned_data['apellidos']}&email={form.cleaned_data['email']}&direccion={form.cleaned_data['direccion']}&ciudad={form.cleaned_data['ciudad']}&codigo_postal={form.cleaned_data['codigo_postal']}&metodo_pago={form.cleaned_data['metodo_pago']}")

            
    else:
        
        # Si es una solicitud GET, inicializa el formulario con los datos de la dirección
        form = PedidoForm(initial={
            'nombre': request.user.first_name,
            'apellidos': detalles_usuario.last_name,
            'email': detalles_usuario.email,
            'direccion': detalles_usuario.direccion,
            'ciudad': detalles_usuario.ciudad,
            'codigo_postal': detalles_usuario.codigo_postal,
            'metodo_pago': detalles_usuario.metodo_pago
        })
        
    return render(request, 'checkout.html', {'elecciones': elecciones, 'form': form, 'precio_total': precio_total })


class PaymentView(View):
    template_name = 'payment_form.html'

    def get(self, request):
        usuario = request.user.id
        elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
        precio_total = sum(eleccion.get_precio_total() for eleccion in elecciones)

        form = PaymentForm()
        return render(request, self.template_name, {'form': form, 'precio_total': precio_total})

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            usuario = request.user.id
            us = request.user
            elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
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
            if response.get('status'):

                nombre = request.GET.get('nombre', '')
                apellidos = request.GET.get('apellidos', '')
                email = request.GET.get('email', '')
                direccion = request.GET.get('direccion', '')
                ciudad = request.GET.get('ciudad', '')
                codigo_postal = request.GET.get('codigo_postal', '')
                metodo_pago = request.GET.get('metodo_pago', '')

                pedido = Pedido.objects.create(usuario=us)
                pedido.nombre = nombre
                pedido.apellidos = apellidos
                pedido.email = email
                pedido.direccion = direccion
                pedido.ciudad = ciudad
                pedido.codigo_postal = codigo_postal
                pedido.metodo_pago = metodo_pago
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