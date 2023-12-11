from django.db import models
from django.urls import reverse
from user.models import User
from pedidos.models import Pedido

class Incidencia(models.Model):
    DESCRIPCION_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]
    ESTADO = [
        ('Sin revisar', 'Sin revisar'),
        ('En revisión', 'En revisión'),
        ('Revisada', 'Revisada'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)
    urgencia = models.CharField(max_length=5, choices=DESCRIPCION_CHOICES)
    estado = models.CharField(max_length=15, choices=ESTADO, default='Sin revisar')

