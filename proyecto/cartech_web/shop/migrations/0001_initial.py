# Generated by Django 5.0 on 2023-12-05 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accesorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('imagen', models.ImageField(default='accesorios/default.jpg', upload_to='accesorios/')),
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
                ('stock', models.IntegerField()),
                ('caballos', models.IntegerField()),
                ('precio_inicial', models.IntegerField()),
                ('imagen', models.ImageField(default='coches/default.jpg', upload_to='coches/')),
            ],
        ),
        migrations.CreateModel(
            name='DireccionUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True)),
                ('codigo_postal', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Eleccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('comprado', models.BooleanField(default=False)),
            ],
        ),
    ]
