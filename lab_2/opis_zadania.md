# Lab 2

`Kontekst jako wejście modelu`

## Cel Labu

Pytanie przewodnie brzmi:

> Co model otrzymał na wejściu i w jaki sposób wpłynęło to na odpowiedź?

W Labie 1 wejście modelu otrzymało lepiej określony kontrakt zadania. Kontrakt wskazywał modelowi, jak ma odpowiadać, ale nadal nie dostarczał brakujących informacji.

W Labie 2 nadal wykorzystywany jest realny model wywoływany przez Groq, lecz zmieniane jest wejście modelu. Porównywane są:

- brak lokalnych danych,
- wszystkie źródła naraz,
- ręcznie wybrany pakiet kontekstu (`context pack`),
- ręcznie wybrany pakiet kontekstu plus dodatkowa instrukcja: "odpowiadaj tylko na podstawie źródeł i wskazuj `source_id` dla ważnych stwierdzeń",
- celowo wadliwy pakiet kontekstu.

Pakiet kontekstu oznacza mały zestaw wybranych źródeł i fragmentów dla jednego pytania. Nazwa `context pack` pojawia się w plikach, aby łatwo powiązać opis zadania z kodem.

Najważniejsze rozróżnienie w tym labie:

1. `context` - dane pokazane modelowi,
2. `instruction` - reguła określająca, jak model ma użyć danych,
3. `answer` - odpowiedź, którą należy sprawdzić względem danych.

Trafny kontekst nie wystarcza sam z siebie. Model musi otrzymać również instrukcję użycia danych, a gotowa odpowiedź nadal wymaga weryfikacji względem źródeł.

## Co Należy Oddać

Należy uzupełnić [imie_nazwisko_2.md](./imie_nazwisko_2.md), zmienić nazwę pliku na własne dane, np. `jan_kowalski_2.md`, oraz wykonać commit z raportem.

Raport należy wypełniać zgodnie z kolejnością kroków poniżej. Przygotowanie pojęciowe służy do zbudowania modelu mentalnego i nie jest przepisywane do raportu. Do raportu trafiają wyniki pracy praktycznej: wybór źródeł, porównanie wariantów, mapowanie dowodów i końcowy werdykt.

## Krok 0. Przygotowanie Pojęciowe

Ten krok wykonać przed częścią praktyczną. Celem jest zrozumienie:

- czym jest kontekst jako wejście modelu,
- czym różni się `context` od `instruction` i `answer`,
- dlaczego strategia "dołącz wszystkie materiały do promptu" nie jest wystarczająca,
- dlaczego źródła mają status, datę i autorytet,
- dlaczego instrukcja ukryta w dokumencie może wpłynąć na model i dlatego stanowi ryzyko,
- jak ręczna praca z pakietem kontekstu przygotowuje do zrozumienia aplikacji, które samodzielnie dobierają i dostarczają modelowi kontekst.

W części praktycznej ręcznie wykonywane są decyzje, które większa aplikacja GenAI może później częściowo automatyzować: wybór źródeł, ustalenie ich priorytetu, złożenie pakietu kontekstu, odrzucenie ryzykownych treści, sprawdzenie odpowiedzi względem źródeł i ocena ograniczeń wyniku.

Należy wykonać poniższe prompty w podanej kolejności.

### Prompt 1

```text
Wyjaśnij poniższe pojęcia prostym językiem dla początkującego programisty:
- context
- instruction
- answer
- pakiet kontekstu (`context pack`)
- aplikacja dostarczająca kontekst modelowi

Dla każdego pojęcia:
1. podaj prostą definicję
2. wskaż, jaki problem pomaga wyjaśnić
3. wskaż, czego nie rozwiązuje
4. podaj mały przykład w asystencie do nauki
5. podaj jedno częste nieporozumienie
```

### Prompt 2

```text
Dla małego asystenta AI do nauki wyjaśnij, jaką pracę wykonują poniższe decyzje:
- wybór kandydatów źródeł
- ustalenie priorytetu źródeł
- budowanie pakietu kontekstu
- filtr bezpieczeństwa
- sprawdzanie dowodów
- ocena odpowiedzi

Dla każdego elementu podaj:
1. co robi w aplikacji GenAI, która przed odpowiedzią dobiera kontekst
2. co jest wykonywane ręcznie w labie zamiast automatyzacji
3. jaki błąd może powstać, jeśli ten element działa słabo
```

### Prompt 3

```text
Utwórz tabelę porównawczą pięciu wariantów wejścia do modelu:
- no_context
- all_context
- selected_context
- selected_context_with_evidence_instruction
- bad_context

Wiersze:
- co model widzi
- co ten wariant ma pokazać
- jaki typ błędu może ujawnić
- jaki dowód powinien zostać wskazany
- czego ten wariant nadal nie dowodzi

Użyj krótkich przykładów z asystenta do nauki.
```

Po wykonaniu trzech promptów należy zadać dodatkowo:

- Dlaczego trafne źródła nie gwarantują trafnej odpowiedzi?
- Czym różni się źródło nieaktualne od źródła ryzykownego?
- Dlaczego instrukcja wewnątrz dokumentu może wpływać na model i przez to stanowić ryzyko?
- Co pokazuje mapowanie dowodów, czego nie pokazuje samo brzmienie odpowiedzi?
- Która część pracy w tym labie dotyczy wyboru źródeł, a która oceny odpowiedzi?

Do części praktycznej należy przejść dopiero wtedy, gdy możliwe jest samodzielne odpowiedzenie na pięć pytań uzupełniających.

**Do raportu:** nic nie wpisywać z tego kroku. Odpowiedzi mają pomóc w rozumieniu kolejnych kroków.

## Krok 1. Uruchomienie Eksperymentu

Praca odbywa się w katalogu [src](./src).

Najważniejsze pliki:

- [src/questions.json](./src/questions.json) - pytania użytkownika,
- [src/sources](./src/sources) - mały korpus źródeł,
- [src/context_packs/selected_contexts.json](./src/context_packs/selected_contexts.json) - trafnie dobrane pakiety kontekstu,
- [src/context_packs/bad_contexts.json](./src/context_packs/bad_contexts.json) - celowo wadliwe pakiety kontekstu,
- [src/run.py](./src/run.py) - uruchamianie eksperymentów,
- [src/outputs/compare.md](./src/outputs/compare.md) - raport porównawczy.

Należy uzupełnić lokalny plik `src/.env` na podstawie `src/.env.example`.

Z katalogu `zadania/lab_2/src` należy uruchomić:

```bash
make doctor
make compare
```

`make compare` zapisuje:

- `outputs/compare.md`,
- `outputs/no_context.md`,
- `outputs/all_context.md`,
- `outputs/selected_context.md`,
- `outputs/selected_context_with_evidence_instruction.md`,
- `outputs/bad_context.md`.

Raporty zawierają pełny input modelu. Jest to celowe: źródła są małe, a pełny input pozwala sprawdzić, co model faktycznie otrzymał.

Głównym plikiem pracy jest `outputs/compare.md`. Pozostałe pliki należy otwierać wtedy, gdy potrzebny jest konkretny dowód:

- `context_packs/*.json` - aby sprawdzić, dlaczego źródło zostało użyte albo odrzucone,
- `sources/*.md` - aby znaleźć dokładny fragment i metadane źródła,
- osobne pliki wariantów w `outputs/` - aby sprawdzić pełny input modelu lub pełną odpowiedź, gdy `compare.md` nie wystarcza.

Wariant `bad_context` nie musi zawsze spowodować błędnej odpowiedzi. Jego celem jest pokazanie, że wadliwy pakiet kontekstu zwiększa ryzyko i wymaga kontroli, a nie udowodnienie, że model zawsze zawiedzie przy złych danych.

**Do raportu:** nie wpisywać samego faktu uruchomienia komend. Wyniki z `outputs/` będą używane w kolejnych krokach.

## Krok 2. Przegląd Pytań, Źródeł i Pakietów Kontekstu

Należy otworzyć:

- `src/outputs/compare.md`.

Celem tego kroku jest zorientowanie się, jakie pytania są badane i jakie warianty wejścia zostały uruchomione. Nie trzeba jeszcze czytać wszystkich źródeł od początku do końca.

Jeżeli `compare.md` wskazuje konkretne źródła, należy wtedy pomocniczo otworzyć:

- `src/context_packs/selected_contexts.json`,
- `src/context_packs/bad_contexts.json`,
- odpowiednie pliki w `src/sources/`.

Dla sprawdzanych źródeł należy zwrócić uwagę na metadane:

- `source_id`,
- `date`,
- `status`,
- `authority`.

Na tym etapie wystarczy zauważyć potencjalne konflikty: dwa źródła mogą mówić o podobnym temacie, ale różnić się datą, statusem, autorytetem albo treścią. Właściwe rozstrzygnięcie konfliktu nastąpi dopiero przy analizie konkretnego pytania.

Przy rozstrzyganiu konfliktu źródeł należy rozpocząć od roboczej reguły:

```text
teacher_email > current_course_doc > course_faq > old_doc > marketing/noise
```

Nie jest to automatyczna prawda. Jest to hipoteza, którą należy uzasadnić datą, statusem, autorytetem i treścią źródła.

Źródło może być mniej przydatne dla danego pytania, jeśli dotyczy innego problemu, jest starsze od innych źródeł o tym samym temacie, ma niższy autorytet, jest sprzeczne z lepszym źródłem albo zawiera ryzykowną treść.

**Do raportu:** na tym etapie jeszcze nic nie przepisywać mechanicznie. Ustalenia z przeglądu zostaną wpisane w krokach 3 i 4.

## Krok 3. Pełna Analiza Przypadku A: `q1_quiz_scope`

Ten przypadek służy do sprawdzenia, jak model radzi sobie z konfliktem między aktualnym źródłem, starszym źródłem i szumem informacyjnym.

Należy:

1. Odczytać pytanie `q1_quiz_scope` w `outputs/compare.md`. Plik `src/questions.json` jest pomocniczym źródłem technicznym.
2. Sprawdzić pakiety dla `q1_quiz_scope` w `selected_contexts.json` i `bad_contexts.json`.
3. Otworzyć źródła wskazane w tych pakietach oraz źródła odrzucone.
4. Ocenić, które źródła są najlepszą podstawą odpowiedzi i dlaczego.
5. Porównać pięć wariantów w `outputs/compare.md` oraz w plikach wariantów:
   - `no_context`,
   - `all_context`,
   - `selected_context`,
   - `selected_context_with_evidence_instruction`,
   - `bad_context`.
6. Sprawdzić w `full_model_input`, co model faktycznie otrzymał.
7. Zmapować 2-3 ważne stwierdzenia odpowiedzi na źródła.

Mapowanie dowodów ma postać:

```text
stwierdzenie z odpowiedzi -> source_id -> dokładny fragment źródła
```

Stwierdzenie z odpowiedzi to pojedyncza informacja, którą można sprawdzić, np. zakres quizu, termin, wyjątek albo zasada feedbacku.

**Do raportu:** wypełnić całą sekcję `1. Przypadek A: q1_quiz_scope`.

## Krok 4. Pełna Analiza Przypadku B: `q3_personalized_plan_limit`

Ten przypadek służy do sprawdzenia, czy model uczciwie rozpoznaje brak danych potrzebnych do personalizacji. Trafny pakiet kontekstu może pomóc, ale nie powinien udawać danych, których nie ma.

Należy:

1. Odczytać pytanie `q3_personalized_plan_limit` w `outputs/compare.md`. Plik `src/questions.json` jest pomocniczym źródłem technicznym.
2. Sprawdzić pakiety dla `q3_personalized_plan_limit` w `selected_contexts.json` i `bad_contexts.json`.
3. Otworzyć źródła wskazane w tych pakietach oraz źródła odrzucone.
4. Ocenić, które źródła są najlepszą podstawą odpowiedzi i czego nadal brakuje.
5. Porównać pięć wariantów w `outputs/compare.md` oraz w plikach wariantów:
   - `no_context`,
   - `all_context`,
   - `selected_context`,
   - `selected_context_with_evidence_instruction`,
   - `bad_context`.
6. Sprawdzić w `full_model_input`, co model faktycznie otrzymał.
7. Zmapować 2-3 ważne stwierdzenia odpowiedzi na źródła.

Jeżeli odpowiedź wydaje się poprawna, ale nie da się jej powiązać ze źródłami, nie stanowi to silnego dowodu. Jeżeli źródła nie wystarczają, należy dokładnie wskazać, czego brakuje.

**Do raportu:** wypełnić całą sekcję `2. Przypadek B: q3_personalized_plan_limit`.

## Krok 5. Szybka Tabela Wszystkich Przypadków

Po pełnej analizie dwóch przypadków należy krótko przejrzeć wszystkie cztery pytania:

- `q1_quiz_scope`,
- `q2_week3_recovery`,
- `q3_personalized_plan_limit`,
- `q4_feedback_rules`.

Dla każdego pytania należy wskazać:

- najlepszy wariant,
- najgorszy albo najbardziej ryzykowny wariant,
- najważniejszy dowód,
- główne ograniczenie.

To nie ma być druga pełna analiza. Dla `q2` i `q4` wystarczy krótka ocena na podstawie `outputs/compare.md`, plików wariantów i źródeł.

**Do raportu:** wypełnić sekcję `3. Szybka Tabela Wszystkich Przypadków`.

## Krok 6. Porównanie Kontekstu, Instrukcji i Odpowiedzi

Należy porównać dwa warianty:

- `selected_context` - model dostaje trafnie dobrane fragmenty,
- `selected_context_with_evidence_instruction` - model dostaje te same fragmenty oraz instrukcję, że ma odpowiadać na podstawie źródeł i wskazywać `source_id`.

Celem nie jest udowodnienie, że sam kontekst zawsze wystarcza albo że sama instrukcja zawsze rozwiązuje problem. Celem jest sprawdzenie, co zmienia dobór danych, a co zmienia instrukcja użycia tych danych.

Uwaga: `all_context` nie musi zawsze być gorszy. Celem nie jest udowodnienie, że duża ilość kontekstu zawsze szkodzi. Duża ilość kontekstu zwiększa jednak odpowiedzialność za selekcję, sprzeczności, aktualność i instrukcje.

**Do raportu:** wypełnić sekcję `4. Kontekst, Instrukcja, Odpowiedź`.

## Krok 7. Ryzykowne Źródło i Prompt Injection

W źródłach znajduje się dokument z instrukcją typu prompt injection.

Instrukcje zapisane wewnątrz dokumentów źródłowych mogą wpływać na model, ponieważ trafiają do jego wejścia jako tekst. To jest problem prompt injection: kontekst może zacząć konkurować z instrukcjami aplikacji i zmieniać odpowiedź w sposób niezamierzony.

Taką treść należy traktować jako dane nie w pełni zaufane: zacytować jako fragment dokumentu, zignorować albo oznaczyć jako ryzyko, ale nie pozwolić jej przejąć sterowania nad odpowiedzią.

Minimalnie należy wskazać:

- `source_id`,
- dokładny ryzykowny fragment,
- dlaczego ten fragment może wpłynąć na model,
- co aplikacja używająca modelu powinna zrobić z tym źródłem.

**Do raportu:** wypełnić sekcję `5. Ryzykowne Źródło`.

## Krok 8. Odrzucenie Słabszego Wyjaśnienia

Należy wybrać jedno kuszące, ale zbyt słabe wyjaśnienie wyniku, np.:

- `selected_context jest lepszy, bo odpowiedź brzmi profesjonalniej`,
- `all_context jest wadliwy, bo duża ilość kontekstu zawsze szkodzi`,
- `model rozwiązał problem, bo podał source_id`,
- `bad_context jest wadliwy tylko dlatego, że ma mniej źródeł`.

Następnie należy odrzucić to wyjaśnienie na podstawie dowodu z `compare.md`, `full_model_input`, źródeł albo mapowania dowodów.

**Do raportu:** wypełnić sekcję `6. Odrzucone Słabsze Wyjaśnienie`.

## Krok 9. Werdykt Końcowy

Na końcu należy wybrać dokładnie jeden werdykt z listy w raporcie i podać najmocniejszy dowód.

Werdykt powinien wynikać z wcześniejszych kroków. Nie wystarcza ogólne stwierdzenie, że odpowiedź "brzmi lepiej". Trzeba wskazać, który wariant miał lepsze dane, lepszą instrukcję, lepsze powiązanie ze źródłami albo uczciwiej nazwał brak danych.

**Do raportu:** wypełnić sekcję `7. Werdykt Końcowy`, zmienić nazwę pliku raportu na własne dane i wykonać commit.
