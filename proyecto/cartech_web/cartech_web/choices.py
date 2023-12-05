from django.db import models


class MetodoPago(models.TextChoices):
        CONTRA_REEMBOLSO =  'contra_reembolso', 'Contra reembolso'
        TARJETA =  'tarjeta', 'Tarjeta'


MetodoPago.choices_with_empty_option = [('', 'Seleccione un método de pago')] + list(MetodoPago.choices)