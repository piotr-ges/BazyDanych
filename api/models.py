from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Model Mieszkaniec
class Mieszkaniec(AbstractUser):
    adres = models.CharField(max_length=255)
    telefon = models.CharField(max_length=15, null=True)
    email = models.EmailField(unique=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.username}"

# Model Licznik
class Licznik(models.Model):
    mieszkaniec = models.ForeignKey(Mieszkaniec, on_delete=models.CASCADE, related_name="liczniki")
    typ_licznika = models.CharField(max_length=50, choices=[("woda", "Woda"), ("gaz", "Gaz"), ("prąd", "Prąd")])  # np. woda, gaz, prąd
    odczyt = models.DecimalField(max_digits=10, decimal_places=2)
    data_odczytu = models.DateField()

    def __str__(self):
        return f"Licznik {self.typ_licznika} dla {self.mieszkaniec}"

# Model Rozliczenie
class Rozliczenie(models.Model):
    STATUS_CHOICES = [
        ('oczekujące', 'Oczekujące'),
        ('zrealizowane', 'Zrealizowane'),
        ('anulowane', 'Anulowane'),
    ]

    mieszkaniec = models.ForeignKey(Mieszkaniec, on_delete=models.CASCADE, related_name="rozliczenia")
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data_rozliczenia = models.DateField()
    opis = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='oczekujące')

    def __str__(self):
        return f"Rozliczenie {self.kwota} PLN dla {self.mieszkaniec} - Status: {self.get_status_display()}"

# Model Usterka
class Usterka(models.Model):
    mieszkaniec = models.ForeignKey(Mieszkaniec, on_delete=models.CASCADE, related_name="usterki")
    opis = models.TextField()
    status = models.CharField(max_length=50, choices=[("nowa", "Nowa"), ("w trakcie", "W trakcie"), ("naprawiona", "Naprawiona")])
    data_zgloszenia = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.opis

# Model Uchwała
class Uchwala(models.Model):
    tytul = models.CharField(max_length=255)
    opis = models.TextField()
    data_przyjecia = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tytul

# Model Harmonogram
class Harmonogram(models.Model):
    tytul = models.CharField(max_length=255)
    data_spotkania = models.DateField()
    czas_spotkania = models.TimeField()
    opis = models.TextField(blank=True, null=True)
    uczestnicy = models.ManyToManyField(Mieszkaniec, related_name="spotkania")

    def __str__(self):
        return f"Spotkanie: {self.tytul} ({self.data_spotkania})"
