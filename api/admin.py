from django.contrib import admin
from . import models

admin.site.register(models.Mieszkaniec)
admin.site.register(models.Licznik)
admin.site.register(models.Harmonogram)
admin.site.register(models.Rozliczenie)
admin.site.register(models.Usterka)
admin.site.register(models.Uchwala)
