# Generated by Django 4.2.7 on 2023-12-02 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_category_id_alter_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accesorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Coche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('combustible', models.CharField(choices=[('gasolina', 'Gasolina'), ('diesel', 'Diesel'), ('hibrido', 'Hibrido'), ('electrico', 'Electrico')], default='gasolina', max_length=20)),
                ('conduccion', models.CharField(choices=[('manual', 'Manual'), ('automatico', 'Automatico')], default='manual', max_length=20)),
                ('consumo', models.FloatField()),
                ('caballos', models.IntegerField()),
                ('precio_inicial', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('contraseña', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Eleccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accesorios', models.ManyToManyField(blank=True, related_name='elecciones', to='shop.accesorio')),
                ('coche', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elecciones', to='shop.coche')),
            ],
        ),
    ]
