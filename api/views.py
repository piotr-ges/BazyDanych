from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import MieszkaniecSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Mieszkaniec

class CreateMieszkaniecView(generics.CreateAPIView):
    queryset = Mieszkaniec
    serializer_class = MieszkaniecSerializer
    permission_classes = [AllowAny]
