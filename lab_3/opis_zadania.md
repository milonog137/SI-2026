# Lab 3: Output Modelu Jako Niezaufane Dane

## Cel Labu

W tym labie pracujesz z malym asystentem kursowym. Model Groq zwraca strukturalny JSON, ale aplikacja nie moze traktowac tego JSON-a jako prawdy. Output modelu jest kolejnym wejsciem systemu: trzeba go sparsowac, sprawdzic mechanicznie, porownac ze zrodlami i dopiero wtedy podjac decyzje.

Glowna petla labu:

```text
baseline -> audyt i naprawa guard -> live run -> analiza trace -> propozycja malej interwencji -> wniosek
```

To zadanie nie polega na poprawianiu promptu tak dlugo, az model odpowie ladnie. Chodzi o zrozumienie, gdzie konczy sie deklaracja modelu, a zaczyna odpowiedzialnosc aplikacji.

## Jak Pracowac Z Raportem

Otworz [imie_nazwisko_3.md](./imie_nazwisko_3.md) przed rozpoczeciem pracy i wypelniaj go po kolei.

Po kazdym kroku w tym opisie znajduje sie pole:

```text
Wpisz teraz do raportu: sekcja ...
```

Wypelnij wskazana sekcje od razu, zanim przejdziesz dalej. Nie zostawiaj raportu na koniec. Raport jest prowadzacym notatnikiem z eksperymentu, a nie osobnym esejem pisanym po fakcie.

## Co Nalezy Oddac

Oddajesz tylko uzupelniony raport:

- skopiuj [imie_nazwisko_3.md](./imie_nazwisko_3.md) albo zmien nazwe pliku na wlasne dane, np. `jan_kowalski_3.md`,
- wypelnij go w trakcie wykonywania krokow,
- wklej do niego wymagane fragmenty zmienionego kodu.

Kod nadal zmieniasz lokalnie, zeby wykonac lab i uruchomic testy. Nie oddajesz osobnego commita ani osobnych plikow z kodem jako artefaktu zadania.

Raport ma opierac sie na:

- wyniku `make doctor`,
- wyniku `make test`,
- naprawie bledow w `src/app/output_guard.py`,
- propozycji jednej malej interwencji po analizie trace,
- `outputs/traces/*.json`,
- `outputs/checks/*.md`,
- `src/sources/`.

## Krok 0. Przygotowanie Pojeciowe

Przeczytaj [intro.md](./intro.md).

Przed czescia praktyczna upewnij sie, ze umiesz wlasnymi slowami odpowiedziec na cztery pytania:

1. Dlaczego poprawny JSON nie oznacza poprawnej odpowiedzi?
2. Dlaczego pola takie jak `status`, `evidence`, `risk_flags` i `next_action` moga byc deklaracjami modelu, a nie decyzja koncowa aplikacji?
3. Co daje trace przy analizie outputu modelu?
4. Jaka jest roznica miedzy poprawnym formatem outputu a poprawna trescia outputu?

Jesli ktorekolwiek pytanie jest niejasne, wroc do [intro.md](./intro.md) albo popros asystenta AI o proste wyjasnienie brakujacego pojecia na przykladzie aplikacji GenAI, w ktorej LLM jest tylko jednym komponentem systemu.

Wpisz teraz do raportu: nic. Ten krok jest tylko przygotowaniem.

## Krok 1. Start I Sprawdzenie Srodowiska

Praca odbywa sie w katalogu [src](./src).

Z katalogu `zadania/lab_3/src` uruchom:

```bash
make doctor
```

`make doctor` sprawdza lokalne pliki i informuje, czy widzi `GROQ_API_KEY`. Jezeli klucz jest obecny, komenda robi tez krotki test polaczenia z Groq. Jezeli klucza nie ma, sekcja live jest pominieta, ale lokalna diagnostyka nadal dziala.

Najwazniejsze pliki, ktore beda potrzebne dalej:

- [src/app/output_guard.py](./src/app/output_guard.py) - glowny plik do audytu i naprawy,
- [src/tests/test_output_guard.py](./src/tests/test_output_guard.py) - testy oczekiwanego zachowania guard,
- [src/system/output_contract.md](./src/system/output_contract.md) - kontrakt outputu modelu,
- [src/system/output_guard_rules.json](./src/system/output_guard_rules.json) - reguly guard,
- [src/sources/](./src/sources) - zrodla, do ktorych model moze sie odwolac,
- `outputs/traces/` - trace'y po `make ask`,
- `outputs/checks/` - raporty guard po `make check`.

Wpisz teraz do raportu: sekcja `1. Start I Srodowisko`.

## Krok 2. Baseline: Zobaczenie Poczatkowego Stanu

Uruchom testy przed jakakolwiek zmiana kodu:

```bash
make test
```

Na poczatku czesc testow ma nie przejsc. To jest zamierzone. System ma wadliwa implementacje warstwy `output guard`.

Twoje zadanie w tym kroku nie polega jeszcze na naprawie. Masz zobaczyc, jakie ryzykowne outputy guard przepuszcza.

Testy wskazuja siedem zachowan, ktore guard powinien wymuszac:

1. brak wymaganego pola ma zatrzymac output,
2. nieznany `status` ma zatrzymac output,
3. nieznane `next_action` ma zatrzymac output,
4. `source_id` musi istniec w katalogu zrodel,
5. `source_id` musi byc jednym ze zrodel przekazanych modelowi w danym wywolaniu,
6. `quote` musi byc dokladnym fragmentem cytowanego zrodla,
7. `unsupported` nie moze miec `next_action = answer_user`.

Wpisz teraz do raportu: sekcja `2. Baseline`.

## Krok 3. Audyt I Naprawa Guard

Otworz:

- [src/tests/test_output_guard.py](./src/tests/test_output_guard.py),
- [src/app/output_guard.py](./src/app/output_guard.py).

Pracuj liniowo:

1. Wez pierwszy failing test z baseline.
2. Znajdz w `output_guard.py` funkcje, ktora powinna pilnowac tego zachowania.
3. Nazwij bledne zalozenie w obecnym kodzie.
4. Wykonaj minimalna poprawke.
5. Powtorz dla kolejnego failing testu.
6. Uruchamiaj `make test`, az wszystkie testy przejda.

Nie zmieniaj:

- `src/app/groq_client.py`,
- `src/app/cli.py`,
- `src/run.py`,
- `src/tests/test_output_guard.py`,
- `src/cases.json`,
- `src/sources/`,
- `src/system/output_contract.md`,
- `src/system/output_guard_rules.json`.

To ograniczenie jest celowe. Zadanie nie polega na obejscu testow ani zmianie danych wejsciowych, tylko na naprawieniu logiki walidacji outputu.

Po naprawie uruchom:

```bash
make test
```

Wpisz teraz do raportu: sekcje `3. Audyt I Naprawa Guard` oraz `3A. Zmieniony Kod Guard`.

## Krok 4. Live Run: Cztery Przypadki

Po przejsciu testow uruchom cztery wymagane przypadki. Po kazdej parze `make ask` + `make check` od razu wypelnij w raporcie wiersz z tym samym `CASE_ID`. Po czwartym przypadku uzupelnij podsumowanie sekcji `4. Live Run`.

```bash
make ask CASE_ID=c1_supported_quiz_scope
make check CASE_ID=c1_supported_quiz_scope
```

```bash
make ask CASE_ID=c2_unsupported_quiz_duration
make check CASE_ID=c2_unsupported_quiz_duration
```

```bash
make ask CASE_ID=c3_partial_week3_recovery
make check CASE_ID=c3_partial_week3_recovery
```

```bash
make ask CASE_ID=c6_prompt_injection_pressure
make check CASE_ID=c6_prompt_injection_pressure
```

Jak wypelnic kazdy wiersz:

- artefakty: sciezki do `outputs/traces/<case_id>.json` i `outputs/checks/<case_id>.md`,
- status: oczekiwany status z tabeli oraz `parsed_output.status` albo wynik z check report,
- next action: `parsed_output.next_action` albo wynik z check report,
- guard / key check: `PASS` albo `ATTENTION` oraz najwazniejszy `FAIL` z check report albo `brak`,
- decyzja aplikacji: jedno zdanie o tym, czy aplikacja moglaby pokazac `answer`, czy powinna zatrzymac output, poprosic o doprecyzowanie albo wymagac recznej kontroli.

Wynik `ATTENTION` nie musi oznaczac bledu implementacji. Moze oznaczac, ze model zwrocil output niezgodny z kontraktem albo wymagajacy recznego osadu.

## Krok 5. Gleboka Analiza Jednego Trace

Wybierz jeden przypadek z sekcji `4. Live Run` do glebszej analizy. Najlepiej wybierz case, ktory bedzie dobrym kandydatem do malej interwencji:

- guard zwrocil `ATTENTION`,
- model pominal istotna flage ryzyka,
- model wybral niejasny `next_action`,
- odpowiedz byla formalnie poprawna, ale trudna do oceny.

Analizujesz tylko jeden przypadek gleboko. Pozostale trzy zostaja opisane w tabeli live run.

Dla wybranego case'a otworz:

- `outputs/traces/<case_id>.json`,
- `outputs/checks/<case_id>.md`,
- odpowiednie pliki z `src/sources/`.

Sprawdz po kolei:

1. Co model dostal w `full_model_input`.
2. Co model zwrocil w `raw_model_output`.
3. Co aplikacja sparsowala w `parsed_output`.
4. Ktore checki przeszly, a ktore nie.
5. Czy `quote` faktycznie wspiera `claim`, a nie tylko istnieje w zrodle.
6. Jaka decyzje powinna podjac aplikacja po analizie.

Wpisz teraz do raportu: sekcja `5. Analiza Wybranego Trace`.

## Krok 6. Propozycja Malej Interwencji

Na podstawie analizy z Kroku 5 zaproponuj jedna mala interwencje. W podstawowej wersji labu nie zmieniasz juz plikow i nie uruchamiasz dodatkowego sprawdzenia po zmianie. Chodzi o to, zeby umiec przejsc od obserwacji w trace do konkretnej, ograniczonej propozycji poprawy systemu.

Propozycja ma byc mala, konkretna i oparta na obserwacji z trace. Nie chodzi o ogolne "poprawienie promptu", tylko o jedna hipoteze, ktora mozna byloby sprawdzic w osobnym eksperymencie.

Dozwolone sa tylko dwa typy propozycji:

1. doprecyzowanie [src/system/output_contract.md](./src/system/output_contract.md), np. instrukcji dotyczacej `risk_flags`, `next_action` albo cytatow,
2. zaostrzenie walidacji w [src/app/output_guard.py](./src/app/output_guard.py), jesli analiza trace pokazuje brak mechanicznego checka.

Nie zmieniaj testow, przypadkow ani zrodel, aby poprawic wynik. W tym kroku nie zmieniaj tez `output_contract.md` ani `output_guard.py`; zapisz tylko propozycje.

Wpisz teraz do raportu: sekcja `6. Propozycja Malej Interwencji`.

## Krok 7. Wniosek Koncowy

Na koniec odpowiedz krotko na dwa pytania:

1. Co oznacza w tym labie zdanie: output modelu jest niezaufanymi danymi?
2. Co pokazala petla: uruchomienie pipeline -> analiza trace/check/source -> decyzja aplikacji -> propozycja interwencji?

Wpisz teraz do raportu: sekcja `7. Wniosek Koncowy`.

## Opcjonalnie: Transfer Na Innym Przypadku

Ta czesc wykonaj tylko po zakonczeniu glownej petli labu. Nie jest wymagana do zaliczenia podstawowej wersji zadania.

Jesli masz czas, wybierz jeszcze jeden przypadek z tabeli live run i przejdz przez skrocona wersje tej samej analizy. Nie musisz implementowac zmiany w kodzie ani robic dodatkowych uruchomien po zmianie. Celem jest sprawdzenie, czy umiesz rozpoznac podobny albo inny typ problemu w drugim wyniku modelu.

Wybierz przypadek, ktory nie byl analizowany gleboko w Kroku 5, i odpowiedz:

1. Co bylo podejrzane albo pouczajace w wyniku?
2. Jaki konkretny fragment trace, check report albo zrodla to pokazuje?
3. Czy problem jest podobny do glownego przypadku, czy inny?
4. Jaka mala zmiane mozna byloby rozwazyc, gdyby ten case mial byc osobnym eksperymentem?
5. Dlaczego nie musi to byc ta sama zmiana co w glownej propozycji?

Wpisz teraz do raportu: opcjonalna sekcja `Transfer Na Innym Przypadku`.

## Czego Nie Zmieniac

Nie zmieniaj testow, przypadkow ani zrodel po to, aby testy lub checki latwiej przechodzily.

Obowiazkowa naprawa dotyczy `src/app/output_guard.py`.

Po naprawie guard w Kroku 3 nie zmieniaj juz plikow systemu w podstawowej wersji labu. W Kroku 6 zapisujesz tylko propozycje interwencji.
