from rest_framework import serializers
from .models import Mieszkaniec, Licznik, Rozliczenie, Usterka, Uchwala, Harmonogram
from rest_framework.authtoken.views import Token


class MieszkaniecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mieszkaniec
        fields = ["id", "username", "first_name", "last_name", "adres", "telefon", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Mieszkaniec(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            adres=validated_data['adres'],
            telefon=validated_data['telefon'],
            email=validated_data['email']
        )
        password = validated_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class LicznikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licznik
        fields = ["id", "mieszkaniec", 'typ_licznika', 'odczyt', 'data_odczytu']

class RozliczenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rozliczenie
        fields = ["id", "mieszkaniec", "kwota", "data_rozliczenia", "opis", "status"]

class UsterkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usterka
        fields = ['id', 'mieszkaniec', 'opis', 'status']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.user.is_staff:
            fields['status'].read_only = False
        else:
            fields['status'].read_only = True
        fields['mieszkaniec'].read_only = True
        return fields

    def validate(self, data):
        try:
            return super().validate(data)
        except serializers.ValidationError as e:
            print(f"Validation error: {e}")
            raise

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




