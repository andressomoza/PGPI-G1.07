from django.shortcuts import render, get_object_or_404
from shop.models import Eleccion, Coche, Accesorio
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CardInformationSerializer  # Make sure to import the serializer
from django.views import View
from .forms import PaymentForm

import stripe

stripe.api_key = 'sk_test_51OJBJcLdnlgk3Y2d9IrdBowToBzxmDRdI2NgP2rTC9tBhTcW2Gebhqllorvp5g1Ru1aSG9Uw1R8k2NN8blJneUyR00Z3eVQBGi'

def home(request):
    return render(request, 'shop/home.html')

# @login_required
def listar_carrito(request):
    usuario = request.user.id
    elecciones = Eleccion.objects.all()
    elecciones = elecciones.filter(usuario_id=usuario)

    for eleccion in elecciones:
        print(eleccion.)

    return render(request, 'listar_carrito.html', {'elecciones': elecciones})


class PaymentView(View):
    template_name = 'payment_form.html'

    def get(self, request):
        form = PaymentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            api_data = {
                'card_number': form.cleaned_data['card_number'],
                'expiry_month': form.cleaned_data['expiry_month'],
                'expiry_year': form.cleaned_data['expiry_year'],
                'cvc': form.cleaned_data['cvc'],
            }

            response = self.stripe_card_payment(data_dict=api_data)

            if response.get('status') == status.HTTP_200_OK:
               return redirect('carrito:listar_carrito')
            else:
                return redirect('carrito:listar_carrito')
        else:
            return render(request, self.template_name, {'form': form})

    def stripe_card_payment(self, data_dict):
        try:
            card_details = {
                "type": "card",
                "card": {
                    "number": data_dict['card_number'],
                    "exp_month": data_dict['expiry_month'],
                    "exp_year": data_dict['expiry_year'],
                    "cvc": data_dict['cvc'],
                },
            }
            # You can also get the amount from the database by creating a model
            payment_intent = stripe.PaymentIntent.create(
                amount=1000,
                currency='eur',
            )
            payment_intent_modified = stripe.PaymentIntent.modify(
                payment_intent['id'],
                payment_method=card_details['id'],
            )
            try:
                payment_confirm = stripe.PaymentIntent.confirm(payment_intent['id'])
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
            except:
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
                payment_confirm = {
                    "stripe_payment_error": "Failed",
                    "code": payment_intent_modified['last_payment_error']['code'],
                    "message": payment_intent_modified['last_payment_error']['message'],
                    'status': "Failed"
                }
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
        except:
            response = {
                'error': "Your card number is incorrect",
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        return response
