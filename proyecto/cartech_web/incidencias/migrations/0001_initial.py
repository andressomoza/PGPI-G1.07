# Generated by Django 4.2.7 on 2023-11-28 19:25

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
                ('descripcion', models.TextField()),
                ('urgencia', models.CharField(choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')], max_length=5)),
            ],
        ),
    ]
