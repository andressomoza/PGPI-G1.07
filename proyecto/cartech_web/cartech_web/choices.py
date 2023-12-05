from django.db import models


class MetodoPago(models.TextChoices):
        CONTRA_REEMBOLSO =  'contra_reembolso', 'Contra reembolso'
        TARJETA =  'tarjeta', 'Tarjeta'