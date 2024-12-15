from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Mieszkaniec


class MieszkaniecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mieszkaniec
        fields = ["id", "username", "imie", "nazwisko", "adres", "telefon", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Mieszkaniec.objects.create_user(**validated_data)
        return user

