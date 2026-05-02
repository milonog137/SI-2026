# Lab 3 `src`

Minimalny system do traktowania outputu modelu jako niezaufanych danych:

```text
case -> context -> model output -> parser -> output guard -> trace -> manual review
```

Podzial odpowiedzialnosci:

- `run.py` - cienki entrypoint uruchamiajacy CLI.
- `app/cli.py` - komendy `doctor`, `ask`, `check`, `run-all`, `snapshot`.
- `app/groq_client.py` - wywolanie API Groq.
- `app/lab_io.py` - ladowanie przypadkow, zrodel, regul, trace'ow i plikow wynikowych.
- `app/prompt_builder.py` - budowanie wiadomosci wysylanych do modelu.
- `app/output_parser.py` - parsowanie surowego tekstu modelu do obiektu JSON.
- `app/output_guard.py` - deterministyczne checki outputu. To jest glowny plik do audytu i naprawy.
- `app/trace_store.py` - budowanie trace'a jednego wywolania.
- `app/report_writer.py` - zapis raportow guard.
- `tests/test_output_guard.py` - testy oczekiwanych zachowan guard.

Podstawowe komendy:

```bash
make doctor
make test
make ask CASE_ID=c1_supported_quiz_scope
make check CASE_ID=c1_supported_quiz_scope
make snapshot CASE_ID=c1_supported_quiz_scope LABEL=before_intervention
```

`make doctor` sprawdza lokalne pliki i pokazuje sekcje live. Jesli `GROQ_API_KEY` jest obecny, sekcja live testuje polaczenie z Groq. Jesli klucza nie ma, sekcja live jest pominieta.

`make test` na poczatku ma pokazac failing tests. Zadanie polega na znalezieniu blednych zalozen w `app/output_guard.py` i naprawieniu guard tak, aby testy przeszly.

`make ask` wymaga `GROQ_API_KEY` w lokalnym pliku `.env`.

`make snapshot` kopiuje aktualny trace oraz raport checkera dla wskazanego case'a do plikow z etykieta, np. `*_before_intervention.*`.
