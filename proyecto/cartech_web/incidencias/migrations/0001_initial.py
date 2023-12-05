# Generated by Django 5.0 on 2023-12-05 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('urgencia', models.CharField(choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')], max_length=5)),
            ],
        ),
    ]
