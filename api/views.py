from rest_framework import status
from .serializers import HarmonogramCreateSerializer
from .serializers import HarmonogramDetailSerializer
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Mieszkaniec, Uchwala, Harmonogram, Usterka, Licznik, Rozliczenie
from .serializers import MieszkaniecSerializer, UchwalaSerializer, HarmonogramSerializer, UsterkaSerializer, LicznikSerializer, RozliczenieSerializer
from .permissions import IsAdminOrReadOnly
from django.contrib.auth import authenticate


class CreateMieszkaniecView(generics.CreateAPIView):
    """
    Tworzy nowego mieszkańca.
    Dostęp: Publiczny (AllowAny).
    """
    queryset = Mieszkaniec.objects.all()
    serializer_class = MieszkaniecSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class MieszkaniecViewSet(viewsets.ModelViewSet):
    """
    Zarządza mieszkańcami.
    - Odczyt: Dostęp dla wszystkich uwierzytelnionych użytkowników.
    - Edycja: Dostęp tylko dla administratorów (superuserów) i właścicieli kont.
    """
    queryset = Mieszkaniec.objects.all()
    serializer_class = MieszkaniecSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Mieszkaniec.objects.all()
        return Mieszkaniec.objects.filter(id=user.id)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
        return super().get_permissions()

    def perform_update(self, serializer):
        if not self.request.user.is_staff and self.request.user != serializer.instance:
            raise PermissionDenied("You can only update your own data.")
        password = serializer.validated_data.get('password', None)
        if password:
            serializer.instance.set_password(password)
        serializer.save()

@api_view(['POST'])
def login(request):
    """
    Loguje użytkownika i zwraca token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UchwalaViewSet(viewsets.ModelViewSet):
    """
    Zarządza uchwałami.
    - Odczyt: Dostęp dla wszystkich uwierzytelnionych użytkowników.
    - Edycja: Dostęp tylko dla administratorów (superuserów).
    """
    queryset = Uchwala.objects.all()
    serializer_class = UchwalaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class UsterkaListCreateView(generics.ListCreateAPIView):
    """
    Zarządza usterkami.
    - Odczyt: Dostęp tylko dla zalogowanego użytkownika.
    - Tworzenie: Dostęp dla wszystkich uwierzytelnionych użytkowników (z wyjątkiem administratorów).
    """
    serializer_class = UsterkaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Usterka.objects.all()
        return Usterka.objects.filter(mieszkaniec=user)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise PermissionDenied("Admins cannot create new issues.")
        try:
            print(f"Creating usterka with data: {serializer.validated_data}")
            serializer.save(mieszkaniec=self.request.user, status='nowa')
        except Exception as e:
            print(f"Error creating usterka: {e}")
            raise


class UsterkaAdminView(generics.RetrieveUpdateAPIView):
    """
    Zarządza usterkami dla administratorów.
    - Odczyt i aktualizacja: Dostęp tylko dla administratorów (superuserów).
    """
    queryset = Usterka.objects.all()
    serializer_class = UsterkaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admins can update issues.")
        try:
            print(f"Updating usterka with data: {serializer.validated_data}")
            serializer.save()
            print(f"Updated usterka: {serializer.instance}")
        except Exception as e:
            print(f"Error updating usterka: {e}")
            raise


class LicznikViewSet(viewsets.ModelViewSet):
    """
    Zarządza licznikami.
    - Odczyt: Dostęp dla wszystkich uwierzytelnionych użytkowników.
    - Edycja: Dostęp tylko dla administratorów (superuserów).
    """
    queryset = Licznik.objects.all()
    serializer_class = LicznikSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Licznik.objects.all()
        return Licznik.objects.filter(mieszkaniec=user)


class RozliczeniaViewSet(viewsets.ModelViewSet):
    """
    Zarządza rozliczeniami.
    - Odczyt: Dostęp dla wszystkich uwierzytelnionych użytkowników.
    - Edycja: Dostęp tylko dla administratorów (superuserów).
    """
    queryset = Rozliczenie.objects.all()
    serializer_class = RozliczenieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Rozliczenie.objects.all()
        return Rozliczenie.objects.filter(mieszkaniec=user)


class UpdateContactInfoView(generics.UpdateAPIView):
    """
    Aktualizuje dane kontaktowe mieszkańca.
    - Edycja: Dostęp dla wszystkich uwierzytelnionych użytkowników.
    """
    queryset = Mieszkaniec.objects.all()
    serializer_class = MieszkaniecSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def getUserInfo(request):
    """
    Zwraca informacje o zalogowanym użytkowniku.
    """
    user = request.user
    if not user.is_authenticated:
        return Response(status=401)
    return Response({
        'id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
    })
class HarmonogramViewSet(viewsets.ModelViewSet):
    queryset = Harmonogram.objects.all()

    # Określenie, który serializer jest używany w zależności od akcji
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HarmonogramDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return HarmonogramCreateSerializer
        return HarmonogramDetailSerializer

    # Ustawienie uprawnień
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]  # Tylko admini mogą dodawać i edytować
        return [IsAuthenticated()]  # Każdy użytkownik może przeglądać listę spotkań

    # Akcja dołączania użytkownika do spotkania
    @action(detail=True, methods=['post'], url_path='register')
    @extend_schema(request=None)
    def register(self, request, pk=None):
        meeting = self.get_object()
        user = request.user
        if user in meeting.uczestnicy.all():
            return Response({'detail': 'Już uczestniczysz w tym spotkaniu.'}, status=status.HTTP_400_BAD_REQUEST)
        meeting.uczestnicy.add(user)
        return Response({'detail': 'Pomyślnie dołączyłeś do spotkania.'})

    # Akcja wypisywania użytkownika ze spotkania
    @action(detail=True, methods=['post'], url_path='unregister')
    @extend_schema(request=None)
    def unregister(self, request, pk=None):
        meeting = self.get_object()
        user = request.user
        if user not in meeting.uczestnicy.all():
            return Response({'detail': 'Nie jesteś uczestnikiem tego spotkania.'}, status=status.HTTP_400_BAD_REQUEST)
        meeting.uczestnicy.remove(user)
        return Response({'detail': 'Pomyślnie opuszczono spotkanie.'})