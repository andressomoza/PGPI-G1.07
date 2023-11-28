from django.db import models
from django.urls import reverse

class Incidencia(models.Model):
    DESCRIPCION_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    descripcion = models.TextField()
    urgencia = models.CharField(max_length=5, choices=DESCRIPCION_CHOICES)

    def __str__(self):
        return f"{self.descripcion} - {self.urgencia}"