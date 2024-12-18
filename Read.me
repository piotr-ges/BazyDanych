# Dokumentacja Backendu - Projekt Bazy Danych

## Opis
Projekt jest napisany w Django i służy do zarządzania operacjami w aplikacji dla mieszkańców. Obejmuje funkcje takie jak:
- Rejestracja użytkowników
- Wyświetlanie liczników
- Zgłaszanie usterek
- Śledzenie harmonogramu
- Rozliczenia

Projekt wykorzystuje Django Rest Framework w celu zapewnienia API zintegrowanego z uwierzytelnianiem.

---

## Technologie użyte
- *Django*
- *Django Rest Framework*
- *Token Authorization*

---

## Linki
- *Admin Panel:* /admin/
- *Rejestracja:* /api/user/register
- *Token Authorization:* /auth/
- *API Root:* /api/
- *API Dokumentacja:*
  - OpenAPI Schema: /api/schema/
  - Swagger UI: /api/schema/swagger-ui/
  - Redoc UI: /api/schema/redoc/

---

## End-pointy

### Liczniki
- Widok mieszkańca: /liczniki/mieszkaniec/
- Widok admina: /liczniki/admin/

### Rozliczenia
- Widok mieszkańca: /rozliczenia/mieszkaniec/
- Widok admina: /rozliczenia/admin/

### Usterki
- Widok mieszkańca: /usterki/mieszkaniec/
- Widok admina: /usterki/admin/

### Harmonogram
- Widok harmonogramu: /spotkania/

---

## Modele

### Mieszkaniec
Rozszerzenie modelu użytkownika o AbstractUser.
- *Pola:*
  - adres
  - telefon
  - email

### Licznik
- *Pola:*
  - mieszkaniec
  - typ_licznika
  - odczyt
  - data_odczytu

### Rozliczenie
- *Pola:*
  - mieszkaniec
  - kwota
  - opis

### Usterka
- *Pola:*
  - mieszkaniec
  - opis
  - status
  - data_zgloszenia

### Harmonogram
- *Pola:*
  - tytul
  - data_spotkania
  - uczestnicy

---

## Serializery
Zdefiniowane w pliku serializers.py, obsługują walidację danych i transformację odpowiedzi API.

### Kluczowe serializery:
- **MieszkaniecSerializer** - przetwarza dane użytkownika
- **LicznikSerializer** - przetwarza dane liczników
- **RozliczenieSerializer** - przetwarza dane rozliczeń
- **UsterkaSerializer** - przetwarza dane usterek
- **HarmonogramSerializer** - przetwarza dane harmonogramu

---

## Widoki
Zdefiniowane w pliku views.py, obsługują logikę API.

### Obsługa użytkownika
- **CreateMieszkaniecView**
- **MieszkaniecViewSet**

### Obsługa liczników
- **LicznikMieszkaniecView**
- **LicznikAdminView**

### Obsługa rozliczeń
- **RozliczenieMieszkaniecView**
- **RozliczenieAdminView**

### Obsługa usterek
- **UsterkaListCreateView**
- **UsterkaAdminView**

### Obsługa harmonogramów
- **HarmonogramViewSet**

---

## Autentykacja i Pozwolenia
- *TokenAuthentication* - używane do dostępu do API.
- *Niestandardowe pozwolenia:*
  - IsAdminOrReadOnly - pozwala na dostęp do odczytu wszystkim zweryfikowanym użytkownikom oraz na zapis tylko administratorom.
  - IsAuthenticated - sprawdza, czy użytkownik jest zalogowany przed udzieleniem dostępu.

---

## Dokumentacja API
- *Swagger UI:* /api/schema/swagger-ui/
- *Redoc UI:* /api/schema/redoc/

---

## Deployment
```bash
python -m venv venv
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
