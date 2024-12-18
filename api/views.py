from rest_framework import generics, viewsets, mixins, status
from .serializers import MieszkaniecSerializer, UchwalaSerializer, LicznikSerializer, RozliczenieSerializer, HarmonogramCreateSerializer
from .serializers import DaneKontaktoweSerializer, LoginSerializer, UsterkaSerializer, HarmonogramSerializer, HarmonogramDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS, IsAdminUser
from .models import Mieszkaniec, Uchwala, Licznik, Rozliczenie, Usterka, Harmonogram
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from rest_framework.decorators import action
class IsAdminOrReadOnly(BasePermission):
    """
    Pozwala na odczyt wszystkim uwierzytelnionym użytkownikom,
    a na edycję tylko administratorom (superuserom).
    """
    def has_permission(self, request, view):
        # Zezwól na odczyt dla wszystkich metod GET, HEAD lub OPTIONS
        if request.method in SAFE_METHODS:
            return True
        # Zezwól na zapis tylko pracownikom
        return request.user and request.user.is_staff

class CreateMieszkaniecView(generics.CreateAPIView):
    """
    Tworzy nowego mieszkańca.
    Dostęp: Publiczny (AllowAny).
    """
    queryset = Mieszkaniec
    serializer_class = MieszkaniecSerializer
    permission_classes = [AllowAny]
class MieszkaniecViewSet(viewsets.ModelViewSet):
    """
    Zarządza mieszkańcami.
    - Odczyt: Dostęp dla wszystkich uwierzytelnionych użytkowników.
    - Edycja: Dostęp tylko dla administratorów (superuserów).
    """
    queryset = Mieszkaniec.objects.all()
    serializer_class = MieszkaniecSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
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

class LicznikMieszkaniecView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    Widok dla mieszkańca: lista i szczegóły liczników zalogowanego użytkownika.
    """
    serializer_class = LicznikSerializer
    permission_classes = [IsAuthenticated]  # Wymaga uwierzytelnienia
    lookup_field = 'id'

    def get_queryset(self):
        """
        Zwraca liczniki przypisane do aktualnie zalogowanego użytkownika.
        """
        return Licznik.objects.filter(mieszkaniec=self.request.user)

    def get(self, request, id=None):
        """
            Obsługuje żądania GET:
        - Jeśli `id` jest podane, zwraca szczegóły wybranego licznika.
        - Jeśli brak `id`, zwraca listę liczników zalogowanego użytkownika.
        """
        if id:
            return self.retrieve(request, id=id)
        return self.list(request)

class LicznikAdminView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    """
    Widok administracyjny dla liczników: pełna kontrola.
    Liczniki są sortowane alfabetycznie po imieniu mieszkańca.
    """
    queryset = Licznik.objects.select_related('mieszkaniec').order_by('mieszkaniec__username')
    serializer_class = LicznikSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class LicznikAdminViewDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    queryset = Licznik.objects.all()
    serializer_class = LicznikSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id=id)

    def put(self, request, id):
        return self.update(request, id=id)

    def delete(self, request, id):
        return self.destroy(request, id=id)

class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request = LoginSerializer,  # Określamy, jakie dane są wymagane w ciele żądania
        responses={200: None, 400: 'Invalid credentials'},  # Określamy odpowiedzi
        description="Logowanie użytkownika i uzyskanie tokenu autoryzacji"
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

    def get(self, request):
        return Response({'detail': 'Please log in.'}, status=405)

class RozliczenieMieszkaniecView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = RozliczenieSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        """
        Zwraca liczniki przypisane do aktualnie zalogowanego użytkownika.
        """
        return Licznik.objects.filter(mieszkaniec=self.request.user)

    def get(self, request, id=None):
        """
            Obsługuje żądania GET:
        - Jeśli `id` jest podane, zwraca szczegóły wybranego Rozliczenia.
        - Jeśli brak `id`, zwraca listę Rozliczeń zalogowanego użytkownika.
        """
        if id:
            return self.retrieve(request, id=id)
        return self.list(request)

class RozliczenieAdminView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):

    queryset = Rozliczenie.objects.select_related('mieszkaniec').order_by('mieszkaniec__username')
    serializer_class = RozliczenieSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id=id)
        return self.list(request)

    def post(self, request):
        return self.create(request)


class RozliczenieAdminViewDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    queryset = Rozliczenie.objects.all()
    serializer_class = LicznikSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id=id)

    def put(self, request, id):
        return self.update(request, id=id)

    def delete(self, request, id):
        return self.destroy(request, id=id)

class UpdateContactInfoView(APIView):
    """
    Widok do aktualizacji danych kontaktowych użytkownika.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=DaneKontaktoweSerializer,  # Określenie serializer do wprowadzenia danych
        responses={200: None},  # Określenie odpowiedzi
        description="Aktualizuje dane kontaktowe użytkownika (email, telefon)."
    )

    def put(self, request):
        """
        Aktualizuje dane kontaktowe (email, telefon) zalogowanego użytkownika.
        """
        serializer = DaneKontaktoweSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Dane kontaktowe zostały zaktualizowane."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsterkaListCreateView(generics.GenericAPIView,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """
    Widok dla usterek: dostęp do listowania i tworzenia usterek
    dla obecnie zalogowanego użytkownika.
    """
    serializer_class = UsterkaSerializer
    permission_classes = [IsAuthenticated]  # Tylko uwierzytelnieni użytkownicy mają dostęp
    authentication_classes = [TokenAuthentication]  # Wymagany token autoryzacji

    def get_queryset(self):
        """
        Zwraca usterki tylko dla aktualnie zalogowanego użytkownika.
        """
        return Usterka.objects.filter(mieszkaniec=self.request.user).order_by('-data_zgloszenia')  # Filtrujemy usterki powiązane z użytkownikiem

    def get(self, request):
        """
        Obsługuje zapytania GET.
        - Zwraca listę usterek aktualnie zalogowanego użytkownika.
        """
        return self.list(request)

    def post(self, request):
        """
        Obsługuje zapytania POST.
        - Tworzy usterkę przypisaną do aktualnie zalogowanego użytkownika.
        """
        user = self.request.user  # Uzyskujemy aktualnie zalogowanego użytkownika
        data = request.data.copy()
        data["mieszkaniec"] = user.id  # Przypisanie użytkownika do zgłoszenia usterki

        data["status"] = "nowa"
        data["data_zgloszenia"] = timezone.now()

        # Walidacja i zapis
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Zapisujemy nową usterkę
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsterkaAdminView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):

    serializer_class = UsterkaSerializer
    queryset = Usterka.objects.select_related('mieszkaniec').order_by('mieszkaniec__username')
    permission_classes = [IsAdminUser]

    def get(self, request):
        return self.list(request)

class UsterkaAdminViewDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):

    queryset = Usterka.objects.all()
    serializer_class = UsterkaSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id=id)

    def put(self, request, id):
        """
        Uaktualnia dane usterki, zachowując przypisanego mieszkańca (mieszkaniec),
        którego usterka dotyczy.
        """
        usterka = self.get_object()  # Pobierz istniejącą usterkę na podstawie ID
        data = request.data.copy()  # Tworzymy kopię danych wejściowych

        # Zachowanie istniejącego mieszkańca, czyli przypisanie do 'mieszkaniec' wartości z istniejącej usterki
        data['mieszkaniec'] = usterka.mieszkaniec.id  # Zachowujemy poprzedniego mieszkańca

        # Serializacja i walidacja
        serializer = self.get_serializer(usterka, data=data, partial=True)  # Partial update

        if serializer.is_valid():
            serializer.save()  # Zapisujemy zaktualizowane dane
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HarmonogramViewSet(viewsets.ModelViewSet):
    queryset = Harmonogram.objects.all()

    # Określenie, który serializer jest używany w zależności od akcji
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HarmonogramDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return HarmonogramCreateSerializer
        return HarmonogramSerializer

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