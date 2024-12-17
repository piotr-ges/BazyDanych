from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import MieszkaniecSerializer, UchwalaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Mieszkaniec, Uchwala
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status, mixins


class CreateMieszkaniecView(generics.CreateAPIView):
    queryset = Mieszkaniec
    serializer_class = MieszkaniecSerializer
    permission_classes = [AllowAny]

class UchwalaList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Uchwala.objects.all()
    serializer_class = UchwalaSerializer

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

class UchwalaDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    queryset = Uchwala.objects.all()
    serializer_class = UchwalaSerializer

    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id=id)

    def put(self, request, id):
        return self.update(request, id=id)

    def delete(self, request, id):
        return self.destroy(request, id=id)




