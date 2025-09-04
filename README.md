# Library API (FastAPI + PostgreSQL + Docker Compose)

Proste API dla systemu bibliotecznego. Umożliwia dodawanie, usuwanie, listowanie książek oraz aktualizację stanu wypożyczenia.

## Uruchomienie

Wymagania:
- Docker + Docker Compose

```bash
docker compose up --build
```
Aplikacja uruchomi się na `http://localhost:8000`. Dokumentacja interaktywna: `http://localhost:8000/docs`

Domyślna konfiguracja bazy danych znajduje się w `.env`.

## Endpoints

- `POST /books` – dodanie nowej książki
- `GET /books` – pobranie listy wszystkich książek
- `DELETE /books/{serial_number}` – usunięcie książki
- `PATCH /books/{serial_number}/status` – wypożyczenie/zwrot

### Walidacja
- Numer seryjny książki: sześciocyfrowy (np. `001234` lub `123456`), unikalny.
- Numer karty bibliotecznej wypożyczającego: sześciocyfrowy.

## Przykłady (curl)

Dodanie książki:
```bash
curl -X POST http://localhost:8000/books -H "Content-Type: application/json" -d '{
  "serial_number": "123456",
  "title": "Solaris",
  "author": "Stanisław Lem"
}'
```

Pobranie listy:
```bash
curl http://localhost:8000/books
```

Wypożyczenie:
```bash
curl -X PATCH http://localhost:8000/books/123456/status -H "Content-Type: application/json" -d '{
  "action": "borrow",
  "borrower_card": "654321"
}'
```

Zwrot:
```bash
curl -X PATCH http://localhost:8000/books/123456/status -H "Content-Type: application/json" -d '{
  "action": "return"
}'
```

Usunięcie:
```bash
curl -X DELETE http://localhost:8000/books/123456
```

## Struktura

- `app/main.py` – definicja FastAPI i endpointów
- `app/database.py` – połączenie z PostgreSQL i ORM
- `app/models.py` – modele SQLAlchemy
- `app/schemas.py` – schematy Pydantic
- `Dockerfile` – obraz aplikacji
- `docker-compose.yml` – uruchomienie aplikacji + PostgreSQL
- `.env` – zmienne środowiskowe

## Notatki
- Brak uwierzytelniania i autoryzacji (wg założeń).
- Tabele są tworzone automatycznie przy starcie aplikacji (bez migracji).
- Czas wypożyczenia (`borrowed_at`) ustawiany automatycznie na czas serwera, jeżeli nie podano.
