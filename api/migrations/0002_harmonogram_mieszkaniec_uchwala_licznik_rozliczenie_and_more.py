# Generated by Django 5.1.4 on 2024-12-14 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Harmonogram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tytul', models.CharField(max_length=255)),
                ('data_spotkania', models.DateField()),
                ('opis', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mieszkaniec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=50)),
                ('nazwisko', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('numer_telefonu', models.CharField(max_length=15)),
                ('adres', models.TextField()),
                ('haslo', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Uchwala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tytul', models.CharField(max_length=255)),
                ('opis', models.TextField()),
                ('data_przyjecia', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Licznik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ_licznika', models.CharField(max_length=50)),
                ('odczyt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_odczytu', models.DateField()),
                ('mieszkaniec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liczniki', to='api.mieszkaniec')),
            ],
        ),
        migrations.CreateModel(
            name='Rozliczenie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kwota', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_rozliczenia', models.DateField()),
                ('opis', models.TextField(blank=True)),
                ('mieszkaniec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rozliczenia', to='api.mieszkaniec')),
            ],
        ),
        migrations.CreateModel(
            name='Usterka',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opis', models.TextField()),
                ('status', models.CharField(choices=[('Nowa', 'Nowa'), ('W trakcie', 'W trakcie'), ('Naprawiona', 'Naprawiona')], max_length=50)),
                ('data_zgloszenia', models.DateField(auto_now_add=True)),
                ('mieszkaniec', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usterki', to='api.mieszkaniec')),
            ],
        ),
    ]