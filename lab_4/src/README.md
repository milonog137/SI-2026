# Laboratorium 4: katalog `src`

Ten katalog zawiera minimalny mechanizm uruchamiania przypadków sprawdzających dla systemu `Study Assistant`.

Skrypt nie ocenia odpowiedzi automatycznie. Jego zadaniem jest wysłanie przypadku do modelu i przygotowanie karty przeglądu, którą student wykorzystuje do ręcznej analizy.

Podstawowy przebieg pracy:

```text
przypadek -> kontrakt Study Assistant -> odpowiedź modelu -> karta przeglądu -> ocena studenta
```

Najważniejsze komendy:

```bash
make doctor
make ask CASE_ID=example_feedback_boundary
make run-student
```

Wywołanie modelu wymaga zmiennej `GROQ_API_KEY`. Można ją ustawić w środowisku albo w lokalnym pliku `.env` w tym katalogu:

```text
GROQ_API_KEY=...
```

W podstawowej wersji ćwiczenia należy edytować tylko plik:

```text
cases/my_cases.json
```

Pliki w `outputs/` są generowane automatycznie. Katalog `outputs/reviews/` zawiera karty przeznaczone do ręcznej analizy odpowiedzi modelu.
