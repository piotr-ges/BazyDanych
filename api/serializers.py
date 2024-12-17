from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Mieszkaniec, Licznik, Rozliczenie, Usterka, Uchwala


class MieszkaniecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mieszkaniec
        fields = ["id", "username", "first_name", "last_name", "adres", "telefon", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Mieszkaniec.objects.create_user(**validated_data)
        return user

class LicznikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licznik
        fields = ["id", "mieszkaniec", 'typ_licznika', 'odczyt', 'data_odczytu']

class RozliczenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rozliczenie
        fields = ["id", "mieszkaniec", "kwota", "data_rozliczenia", "opis"]

class UsterkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usterka
        fields = ['id', 'mieszkaniec', 'opis', 'status', 'data_zgloszenia']

class UchwalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uchwala
        fields = ["id", "tytul", "opis", "data_przyjecia"]




