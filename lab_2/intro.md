# Lab 2 Intro: Kontekst Jako Wejście Modelu

Dokument stanowi wprowadzenie do pojęć oraz elementów kodu wykorzystywanych w Labie 2.

Dotychczasowe doświadczenie z GenAI często zaczyna się od chatbota: użytkownik wpisuje wiadomość, a gotowa aplikacja zwraca odpowiedź. W takim ujęciu łatwo utożsamić LLM z całą aplikacją. W tej części kursu przyjmowana jest inna perspektywa: LLM jest komponentem większej aplikacji GenAI, a nie całą aplikacją.

Z tej perspektywy istotny jest nie tylko sam model, lecz także kod i proces wokół niego: przygotowanie wejścia, wybór danych, dodanie instrukcji oraz zapisanie śladu wywołania. Model generuje odpowiedź na podstawie informacji zapisanych w parametrach sieci neuronowej/LLM oraz danych dołączonych do wejścia w konkretnym wywołaniu. Zmiana wejścia może więc zmienić odpowiedź tego samego modelu.

Jeżeli LLM jest elementem aplikacji, wejście do modelu jest zwykle przygotowywane programistycznie: aplikacja decyduje, jakie pytanie, instrukcje i fragmenty danych zostaną wysłane w konkretnym wywołaniu. Lab 2 koncentruje się na tym etapie. Jest on wykonywany ręcznie, aby widoczne były decyzje, które później może przejąć kod.

Przez aplikację wokół modelu rozumiany jest kod, który przygotowuje wiadomości, dołącza wybrane fragmenty źródeł dla danego pytania i wysyła wywołanie do Groq. W Labie 2 tę rolę pełni głównie `src/run.py`.

## 1. Rola Kodu

Kod w `src/run.py` składa wejście modelu na podstawie kilku plików:

- `src/questions.json` - pytania użytkownika,
- `src/sources/` - lokalne źródła,
- `src/context_packs/selected_contexts.json` - trafnie dobrane pakiety kontekstu,
- `src/context_packs/bad_contexts.json` - celowo wadliwe pakiety kontekstu,
- `src/experiment_variants.json` - konfiguracja wariantów wejścia modelu.

Po uruchomieniu eksperymentu kod zapisuje pełne wejście wysłane do modelu jako `full_model_input`. Jest to istotny ślad techniczny: pokazuje nie całą zawartość repozytorium, lecz dokładnie to, co trafiło do wywołania Groq.

## 2. Pliki Muszą Trafić Do Wejścia Modelu

Pliki w repozytorium nie są częścią wejścia modelu tylko dlatego, że istnieją w katalogu projektu. Sam model nie widzi katalogu `sources/`, zawartości plików ani wcześniejszych decyzji, jeżeli kod nie dołączy ich do wiadomości wysyłanej do Groq.

Model odpowiada na podstawie:

- informacji zapisanych w parametrach sieci neuronowej/LLM,
- instrukcji nadrzędnej ustawionej przez aplikację,
- pytania użytkownika,
- kontekstu dołączonego do wejścia,
- wcześniejszych wiadomości, jeżeli zostały dołączone do wejścia.

## 3. Context, Instruction, Answer

W Labie 2 istotne są trzy odrębne warstwy:

| Warstwa | Znaczenie |
| --- | --- |
| `context` | Dane pokazane modelowi, np. fragmenty źródeł. |
| `instruction` | Reguła określająca, jak model ma użyć danych. |
| `answer` | Wynik działania modelu, który można sprawdzić względem danych. |

Samo dołączenie trafnych źródeł nie gwarantuje poprawnej odpowiedzi. Model może pominąć ważny fragment, nie oznaczyć braków albo sformułować odpowiedź sugerującą wiedzę szerszą niż ta, która wynika ze źródeł.

Dlatego w kodzie istnieją dwa podobne warianty:

- `selected_context` - model otrzymuje trafnie dobrane fragmenty,
- `selected_context_with_evidence_instruction` - model otrzymuje te same fragmenty oraz instrukcję, że ma odpowiadać na podstawie źródeł i wskazywać `source_id`.

Różnica między tymi wariantami pokazuje, że instrukcja użycia danych jest osobną częścią wejścia modelu.

## 4. Pakiet Kontekstu

Pakiet kontekstu, w plikach nazwany `context pack`, to roboczy pakiet danych dla jednego pytania. Nie jest to cała wiedza aplikacji. Jest to wybrany zestaw informacji, który kod wokół modelu dołącza do konkretnego wywołania.

W Labie 2 taki pakiet zawiera:

- wybrane źródła,
- dokładne fragmenty,
- uzasadnienie użycia,
- ryzyko lub ograniczenie,
- źródła odrzucone,
- znane braki.

Warianty `selected_context` i `bad_context` używają dwóch różnych typów pakietów:

- `selected_contexts.json` zawiera pakiety dobrane tak, aby wspierały odpowiedź na pytanie,
- `bad_contexts.json` zawiera pakiety celowo wadliwe, np. oparte na źródle nieaktualnym, informacyjnym szumie albo dokumencie ryzykownym.

## 5. Warianty Wejścia Modelu

Plik `src/experiment_variants.json` definiuje pięć wariantów:

| Wariant | Co trafia do wejścia modelu | Co ilustruje wariant |
| --- | --- | --- |
| `no_context` | Samo pytanie użytkownika. | Odpowiedź bez lokalnych danych. |
| `all_context` | Wszystkie źródła naraz. | Wpływ dużej ilości danych, szumu i sprzeczności. |
| `selected_context` | Trafnie dobrane fragmenty. | Wpływ selekcji źródeł. |
| `selected_context_with_evidence_instruction` | Te same fragmenty plus instrukcja dowodowa. | Różnicę między danymi a instrukcją użycia danych. |
| `bad_context` | Celowo wadliwy pakiet kontekstu. | Wpływ nietrafnych albo ryzykownych danych. |

`all_context` nie jest z definicji gorszy od krótszego kontekstu. Ważniejszy problem polega na tym, że większa ilość danych zwiększa odpowiedzialność za selekcję, aktualność, sprzeczności, autorytet źródeł i instrukcję użycia danych.

## 6. Decyzje Kontekstowe

Większa aplikacja GenAI może automatyzować część pracy związanej z kontekstem, ale sama praca składa się z kilku odrębnych decyzji:

| Decyzja procesu | Znaczenie |
| --- | --- |
| Wybór kandydatów | Które źródła mogą być przydatne dla pytania. |
| Priorytet źródeł | Które źródła są aktualne, wiarygodne i najlepiej dopasowane. |
| Budowanie pakietu kontekstu | Które fragmenty źródeł trafią do wejścia modelu. |
| Filtr bezpieczeństwa | Które źródła są nieaktualne, szumowe, sprzeczne albo ryzykowne. |
| Sprawdzanie dowodów | Które konkretne stwierdzenia z odpowiedzi da się powiązać ze źródłami. |
| Ocena odpowiedzi | Co odpowiedź rozstrzyga, a czego nadal nie dowodzi. |

Te decyzje są niezależne od konkretnej techniki automatyzacji. Punktem wyjścia jest pytanie, jaki kontekst powinien trafić do wejścia modelu.

## 7. Priorytet Źródeł

Źródła nie są równoważne. Stary dokument może być precyzyjny, ale nieaktualny. Notatka marketingowa może być przekonująca stylistycznie, ale nie rozstrzygać lokalnego pytania. Mail prowadzącego może mieć większy autorytet niż wcześniejsza notatka.

Robocza reguła priorytetu używana w labie:

```text
teacher_email > current_course_doc > course_faq > old_doc > marketing/noise
```

Nie jest to reguła absolutna. Stanowi punkt wyjścia do analizy dwóch cech źródeł:

- `authority` - kto jest wiarygodnym autorem źródła,
- `freshness` - czy źródło jest aktualne względem innych źródeł.

## 8. Prompt Injection W Źródłach

Dokument źródłowy może zawierać tekst wyglądający jak polecenie:

```text
Zignoruj poprzednie polecenia...
```

Prompt injection polega na tym, że dokument źródłowy zawiera tekst próbujący sterować zachowaniem modelu. Dla modelu jest to nadal fragment wejścia, więc może wpłynąć na odpowiedź tak, jakby był instrukcją. To jest ryzyko: kontekst nie jest neutralnym dodatkiem do promptu, lecz częścią wejścia, która może konkurować z instrukcjami aplikacji.

Dlatego aplikacja musi traktować treść dokumentów jako dane nie w pełni zaufane. Instrukcje znalezione w źródłach powinny być oddzielone od instrukcji przygotowanych przez aplikację, oznaczone jako ryzyko, zignorowane albo zacytowane jako treść dokumentu, ale nie powinny przejmować sterowania nad odpowiedzią.

Jest to przykład szerszego problemu: kontekst nie staje się bezpieczny wyłącznie dlatego, że ma postać tekstu.

## 9. Mapowanie Dowodów

Mapowanie dowodów jest prostą metodą walidacji odpowiedzi modelu względem kontekstu. Jego sens jest praktyczny: sprawdzić, czy ważne stwierdzenia w odpowiedzi faktycznie wynikają ze źródeł pokazanych modelowi.

W Labie 2 mapowanie dowodów służy do porównania wariantów wejścia modelu. Nie chodzi o ocenę stylu odpowiedzi, lecz o powiązanie tego, co model stwierdził, z dokumentem, który to potwierdza.

Nie jest to metoda idealna. Mapowanie dowodów może pokazać, że dane stwierdzenie ma podstawę w źródle, ale nie gwarantuje, że cała odpowiedź jest kompletna, dobrze zinterpretowana albo wystarczająca dla użytkownika. Jest to jednak użyteczny punkt startu, ponieważ wymusza sprawdzenie relacji między odpowiedzią a kontekstem.

Silny dowód ma postać:

```text
stwierdzenie z odpowiedzi -> source_id -> dokładny fragment źródła
```

Stwierdzenie z odpowiedzi to pojedyncza informacja, którą można sprawdzić, np. zakres quizu, termin, wyjątek albo zasada feedbacku.

Przykład:

```text
Quiz 2 obejmuje pętle while -> D1_current_quiz_scope -> "Quiz 2 obejmuje dokładnie dwa tematy: pętle `while` oraz list comprehensions."
```

Nie wystarcza samo wrażenie, że odpowiedź jest poprawna. Istotne jest powiązanie konkretnego stwierdzenia z właściwym źródłem i dokładnym fragmentem.

## 10. Główna Lekcja

Model wywoływany przez Groq pozostaje ten sam. Zmienia się wejście wysłane do modelu.

Jakość odpowiedzi zależy od kilku odrębnych decyzji:

- które źródła zostały wybrane jako przydatne dla pytania,
- które konkretne fragmenty tych źródeł pokazano modelowi,
- jaką instrukcję dodano, aby model wiedział, jak użyć źródeł,
- które źródła odrzucono jako nieaktualne, nietrafne albo ryzykowne,
- czy odpowiedź można powiązać z konkretnymi źródłami i fragmentami.

Aplikacja GenAI nie jest wyłącznie modelem. Obejmuje także kod, który przygotowuje wejście modelu i decyduje, jakie dane, instrukcje oraz ograniczenia znajdą się w konkretnym wywołaniu.
