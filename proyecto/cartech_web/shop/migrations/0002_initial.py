# Generated by Django 5.0 on 2023-12-05 21:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('opiniones', '0002_initial'),
        ('pedidos', '0002_initial'),
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='direccionusuario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eleccion',
            name='accesorios',
            field=models.ManyToManyField(blank=True, related_name='elecciones', to='shop.accesorio'),
        ),
        migrations.AddField(
            model_name='eleccion',
            name='coche',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elecciones', to='shop.coche'),
        ),
        migrations.AddField(
            model_name='eleccion',
            name='opinion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='opiniones.opinion'),
        ),
        migrations.AddField(
            model_name='eleccion',
            name='pedido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='elecciones', to='pedidos.pedido'),
        ),
        migrations.AddField(
            model_name='eleccion',
            name='usuario',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
