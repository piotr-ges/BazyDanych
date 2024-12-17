from rest_framework import generics, viewsets
from .serializers import MieszkaniecSerializer, UchwalaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
from .models import Mieszkaniec, Uchwala
from rest_framework.authentication import TokenAuthentication

class IsAdminOrReadOnly(BasePermission):
    """
    Pozwala na odczyt wszystkim uwierzytelnionym użytkownikom,
    a na edycję tylko administratorom (superuserom).
    """
    def has_permission(self, request, view):
        # Zezwól na odczyt dla wszystkich metod GET, HEAD lub OPTIONS
        if request.method in SAFE_METHODS:
            return True
        # Zezwól na zapis tylko superuserom
        return request.user and request.user.is_superuser

class CreateMieszkaniecView(generics.CreateAPIView):
    queryset = Mieszkaniec
    serializer_class = MieszkaniecSerializer
    permission_classes = [AllowAny]

class MieszkaniecViewSet(viewsets.ModelViewSet):
    queryset = Mieszkaniec.objects.all()
    serializer_class = MieszkaniecSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class UchwalaViewSet(viewsets.ModelViewSet):
    queryset = Uchwala.objects.all()
    serializer_class = UchwalaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

'''
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
'''



