from rest_framework import serializers
from .models import Mieszkaniec, Licznik, Rozliczenie, Usterka, Uchwala, Harmonogram
from rest_framework.authtoken.views import Token


class MieszkaniecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mieszkaniec
        fields = ["id", "username", "first_name", "last_name", "adres", "telefon", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Mieszkaniec.objects.create_user(**validated_data)
        Token.objects.create(user=user)
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
        fields = ['id', 'mieszkaniec', 'opis', 'status']
        read_only_fields = ['mieszkaniec']

class UchwalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uchwala
        fields = ["id", "tytul", "opis", "data_przyjecia"]

class DaneKontaktoweSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mieszkaniec
        fields = ["email", "telefon"]

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mieszkaniec
        fields = ["username", "password"]

class MieszkaniecSpotkanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mieszkaniec
        fields = ['id', 'first_name', 'last_name']

class HarmonogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harmonogram
        fields = ['id', 'tytul', 'data_spotkania', 'czas_spotkania']

class HarmonogramDetailSerializer(serializers.ModelSerializer):
    uczestnicy = MieszkaniecSpotkanieSerializer(many=True)
    class Meta:
        model = Harmonogram
        fields = ['id', 'tytul', 'opis', 'data_spotkania', 'czas_spotkania', 'uczestnicy']

class HarmonogramCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harmonogram
        fields = ['tytul', 'opis', 'data_spotkania', 'czas_spotkania']




