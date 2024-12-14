from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

# Model Mieszkaniec
class Mieszkaniec(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    numer_telefonu = models.CharField(max_length=15)
    adres = models.TextField()
    haslo = models.CharField(max_length=128)  # Hasło przechowywane w formie zaszyfrowanej

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

# Model Licznik
class Licznik(models.Model):
    mieszkaniec = models.ForeignKey(Mieszkaniec, on_delete=models.CASCADE, related_name="liczniki")
    typ_licznika = models.CharField(max_length=50)  # np. woda, gaz, prąd
    odczyt = models.DecimalField(max_digits=10, decimal_places=2)
    data_odczytu = models.DateField()

    def __str__(self):
        return f"Licznik {self.typ_licznika} dla {self.mieszkaniec}"

# Model Rozliczenie
class Rozliczenie(models.Model):
    mieszkaniec = models.ForeignKey(Mieszkaniec, on_delete=models.CASCADE, related_name="rozliczenia")
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data_rozliczenia = models.DateField()
    opis = models.TextField(blank=True)

    def __str__(self):
        return f"Rozliczenie {self.kwota} PLN dla {self.mieszkaniec}"

# Model Usterka
class Usterka(models.Model):
    mieszkaniec = models.ForeignKey(Mieszkaniec, on_delete=models.SET_NULL, null=True, blank=True, related_name="usterki")
    opis = models.TextField()
    status = models.CharField(max_length=50, choices=[("Nowa", "Nowa"), ("W trakcie", "W trakcie"), ("Naprawiona", "Naprawiona")])
    data_zgloszenia = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Usterka: {self.opis[:30]} ({self.status})"

# Model Uchwała
class Uchwala(models.Model):
    tytul = models.CharField(max_length=255)
    opis = models.TextField()
    data_przyjecia = models.DateField()

    def __str__(self):
        return self.tytul

# Model Harmonogram
class Harmonogram(models.Model):
    tytul = models.CharField(max_length=255)
    data_spotkania = models.DateField()
    opis = models.TextField(blank=True)

    def __str__(self):
        return f"Spotkanie: {self.tytul} ({self.data_spotkania})"
