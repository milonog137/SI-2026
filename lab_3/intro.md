# Lab 3 Intro: Output Modelu Jako Niezaufane Dane

Lab 1 dotyczy tego, jak rozmawiac z modelem i obserwowac jego zachowanie. Lab 2 dotyczy tego, jaki kontekst trafia do modelu. Lab 3 dodaje kolejna perspektywe systemowa: odpowiedz modelu nie jest jeszcze gotowym faktem ani bezpieczna decyzja aplikacji. Jest outputem, ktory aplikacja musi potraktowac jak niezaufane dane.

W aplikacjach GenAI LLM jest jednym z komponentow systemu. Aplikacja przygotowuje wejscie, wysyla je do modelu, odbiera output i dopiero potem decyduje, co z nim zrobic. Ten ostatni etap jest krytyczny, bo output moze wygladac przekonujaco, ale byc niepoprawny, niezgodny z kontraktem, niesprawdzalny albo ryzykowny.

## 1. Kontekst

W tym labie analizowany jest fragment asystenta kursowego dla studentow. Asystent odpowiada na pytania o zakres quizu, nadrabianie materialu, zasady feedbacku i planowanie nauki na podstawie lokalnych zrodel kursowych.

Nie jest to jeszcze pelna aplikacja. Lab pokazuje jeden jej komponent: warstwe, ktora odbiera output modelu i sprawdza, czy aplikacja moze go bezpiecznie wykorzystac.

Przeplyw w labie jest nastepujacy:

```text
pytanie + zrodla -> Groq -> raw output -> parser -> trace -> output guard -> raport
```

| Etap | Co oznacza w labie |
| --- | --- |
| `pytanie + zrodla` | Pytanie studenta oraz wybrane dokumenty kursowe przekazane do modelu. |
| `Groq` | Wywolanie modelu przez gotowego klienta API. |
| `raw output` | Surowy tekst zwrocony przez model, zanim aplikacja go zinterpretuje. |
| `parser` | Kod, ktory probuje zamienic surowy output na obiekt JSON. |
| `trace` | Zapis wywolania: pytanie, zrodla, input modelu, raw output i parsed output. |
| `output guard` | Kod, ktory sprawdza pola, statusy, `source_id`, `quote` i reguly akcji. |
| `raport` | Wynik checkow oraz miejsce na reczny osad studenta. |

`Trace` oznacza zapis jednego wywolania: pytanie, zrodla pokazane modelowi, surowy output, sparsowany output i wyniki pozniejszych checkow.

Trace jest dziennikiem przebiegu pipeline'u dla jednego przypadku. Pozwala odtworzyc, co dokladnie dostal model, co zwrocil, jak parser zinterpretowal output i ktore checki pozniej przeszly albo nie przeszly. Bez trace'a trudno odroznic blad modelu od bledu kontekstu, parsera, kontraktu outputu albo guard.

W klasycznym oprogramowaniu nie ufa sie bezposrednio danym od uzytkownika ani odpowiedziom z zewnetrznych API. Najpierw sprawdza sie format, pola, typy, zakresy wartosci i uprawnienia. Output modelu nalezy traktowac podobnie.

## 2. Po Co JSON W Asystencie Kursowym

Asystent kursowy nie ma tylko napisac ladnego akapitu. Ma wygenerowac dane, na ktorych aplikacja moze pracowac programistycznie.

Przyklad: student pyta, ile trwa quiz 2. Jezeli zrodla kursowe nie zawieraja czasu trwania ani liczby pytan, aplikacja nie powinna pokazac zmyslonej odpowiedzi. Potrzebuje informacji, ze brakuje danych i ze nastepna akcja powinna byc prosba o doprecyzowanie albo odeslanie do prowadzacego.

Dlatego w tym labie model zwraca JSON. Gdy model zwraca zwykly akapit tekstu, aplikacja musialaby zgadywac, ktora czesc jest odpowiedzia, ktora czesc jest ostrzezeniem, czy brakuje danych i jaka akcja powinna nastapic dalej. JSON zamienia output modelu w jawne pola, na ktorych kod moze pracowac programistycznie: `status`, `risk_flags`, `evidence` i `next_action`.

JSON nie jest tekstem finalnym dla studenta. Jest wewnetrznym formatem wymiany danych miedzy modelem a aplikacja. Po walidacji aplikacja moze uzyc pol JSON-a w prostych regulach. Na przyklad gdy `status = unsupported` i `risk_flags` zawiera `missing_data`, aplikacja nie pokazuje odpowiedzi jako pewnej informacji, tylko prosi uzytkownika o doprecyzowanie. Gdy `status = supported` i `next_action = answer_user`, aplikacja moze pokazac `answer`, o ile guard nie wykryl problemow.

## 3. Kontrakt Outputu

Kontrakt outputu nadaje odpowiedzi strukture, ktora mozna sprawdzic programistycznie. Nie gwarantuje, ze model ma racje. Sprawia tylko, ze output ma jawne pola, ktore aplikacja moze parsowac, walidowac, testowac i logowac.

W tym labie model ma zwrocic obiekt JSON z polami:

```json
{
  "answer": "...",
  "status": "supported | partial | unsupported",
  "evidence": [
    {
      "claim": "...",
      "source_id": "...",
      "quote": "..."
    }
  ],
  "risk_flags": ["missing_data | unsafe_source | prompt_injection | unsupported_claim | none"],
  "next_action": "answer_user | ask_clarifying_question | refuse"
}
```

Znaczenie pol w asystencie kursowym:

| Pole | Sens |
| --- | --- |
| `answer` | Kandydat odpowiedzi dla studenta, np. krotka informacja o zakresie quizu. |
| `status` | Deklaracja modelu, czy odpowiedz ma wystarczajaca podstawe w lokalnych zrodlach kursowych. |
| `evidence` | Slad, na ktore stwierdzenia, zrodla i cytaty powoluje sie output. |
| `risk_flags` | Sygnaly ryzyka, np. brak danych, ryzykowne zrodlo albo prompt injection. |
| `next_action` | Sugestia modelu dotyczaca nastepnej akcji. Nie jest to finalna decyzja aplikacji. |

`claim` oznacza pojedyncze stwierdzenie z odpowiedzi, np. "quiz 2 obejmuje petle while". `source_id` oznacza identyfikator zrodla. `quote` oznacza dokladny fragment zrodla, ktory ma byc podstawa danego stwierdzenia.

Wazne: `status`, `evidence`, `risk_flags` i `next_action` sa deklaracjami modelu. Aplikacja nie przyjmuje ich automatycznie jako prawdy. Dopiero kod, reguly i ewentualny osad czlowieka decyduja, czy odpowiedz mozna pokazac studentowi, czy trzeba poprosic o doprecyzowanie, odmowic albo zatrzymac wynik.

### Przykladowy Slice Systemu

Slice oznacza jedno przejscie przez system dla jednego pytania.

Student pyta:

```text
Ile minut trwa quiz 2 i ile bedzie pytan?
```

Aplikacja dolacza do modelu wybrane zrodla, np.:

```text
D1_current_quiz_scope - aktualny zakres quizu 2
D3_known_gaps - znane braki danych
```

W zrodlach jest informacja o tematach quizu, ale nie ma liczby minut ani liczby pytan. Model moze zwrocic taki JSON:

```json
{
  "answer": "W dostepnych zrodlach nie ma informacji o czasie trwania quizu 2 ani liczbie pytan.",
  "status": "unsupported",
  "evidence": [
    {
      "claim": "Zrodla nie podaja liczby minut ani liczby pytan.",
      "source_id": "D3_known_gaps",
      "quote": "Dla pytania o czas trwania quizu 2 brakuje danych: zrodla nie podaja liczby minut ani liczby pytan."
    }
  ],
  "risk_flags": ["missing_data"],
  "next_action": "ask_clarifying_question"
}
```

`output guard` sprawdza wtedy mechanicznie, czy JSON ma wymagane pola, czy `status` i `next_action` maja dozwolone wartosci, czy `D3_known_gaps` bylo w kontekscie oraz czy `quote` rzeczywiscie wystepuje w tym zrodle. Jezeli checki przejda, aplikacja nadal nie traktuje odpowiedzi jako informacji o czasie quizu. Moze pokazac studentowi komunikat o braku danych albo poprosic o doprecyzowanie, zamiast zgadywac liczbe minut i pytan.

## 4. Uproszczenie Dydaktyczne

W tym labie model zwraca kilka deklaracji w jednym JSON-ie, aby bylo widac, co aplikacja musi potem sprawdzic. To jest uproszczenie.

W bardziej rozbudowanym systemie czesc informacji moze pochodzic z innych komponentow:

- `source_id` moze pochodzic z modulu wyboru zrodel,
- fragmenty kontekstu moga pochodzic z kodu skladajacego kontekst,
- status finalny moze pochodzic z walidatorow,
- decyzja koncowa moze pochodzic z warstwy regul aplikacji.

Model nie powinien byc jedynym zrodlem prawdy o tym, czy odpowiedz jest wsparta, bezpieczna i gotowa do pokazania. Lab celowo pokazuje deklaracje modelu, aby potem bylo jasne, dlaczego trzeba je walidowac.

## 5. Dlaczego Sam JSON Nie Wystarcza

Nawet gdy output ma postac JSON-a, jego tresc nadal moze byc bledna albo niebezpieczna. JSON opisuje strukture danych, ale nie gwarantuje, ze wartosci w polach sa prawdziwe, dozwolone albo oparte na pokazanym kontekscie.

Model moze:

- zwrocic zwykly tekst mimo tego, ze aplikacja oczekuje JSON-a,
- pominac wymagane pole,
- wpisac nieznana wartosc `status`,
- wpisac w polu `source_id` zrodlo, ktore nie istnieje,
- wpisac w polu `source_id` zrodlo, ktore istnieje w katalogu, ale nie bylo pokazane modelowi w tym wywolaniu,
- wpisac w polu `quote` cytat, ktory nie wystepuje w cytowanym zrodle,
- wpisac w polu `answer` odpowiedz mimo braku danych,
- wpisac `next_action = answer_user`, chociaz `status = unsupported`,
- potraktowac instrukcje ukryta w dokumencie z kontekstu jak polecenie systemowe.

Problem nie polega tylko na tym, ze model moze sie mylic. Problem polega na tym, ze aplikacja moze bez kontroli przekazac ten output dalej: do uzytkownika, do bazy danych, do narzedzia, do maila, do workflow albo do kolejnego kroku agenta.

Uwaga: w prawdziwych API czesc systemow korzysta ze structured output albo JSON schema, aby latwiej uzyskac output zgodny ze schematem. To pomaga z formatem, ale nie rozstrzyga, czy wartosci w polach sa prawdziwe. Nawet przy structured output aplikacja nadal musi sprawdzic `source_id`, `quote`, `status`, `risk_flags` i `next_action`.

## 6. Output Guard

Warstwa, ktora sprawdza output modelu, jest w tym labie nazwana `output guard`. Nie jest to drugi model oceniajacy pierwszy model. Jest to zwykly kod, ktory wykonuje deterministyczne checki.

`output guard` moze sprawdzic m.in.:

- czy output da sie sparsowac jako JSON,
- czy wymagane pola istnieja,
- czy `status`, `risk_flags` i `next_action` maja dozwolone wartosci,
- czy `source_id` istnieje w katalogu zrodel,
- czy `source_id` byl rzeczywiscie w kontekscie przekazanym modelowi,
- czy `quote` jest dokladnym fragmentem cytowanego zrodla,
- czy `unsupported` nie jest jednoczesnie przekazywane jako zwykla odpowiedz do uzytkownika.

To sa checki mechaniczne. Sa wazne, bo lapia bledy, ktore da sie wykryc bez interpretowania znaczenia calej odpowiedzi.

## 7. Granica Tego Labu

Ten lab nie rozstrzyga automatycznie, czy cytat logicznie wspiera stwierdzenie. To wymaga oceny semantycznej. Taka ocena moze byc wykonywana przez czlowieka, reguly domenowe, klasyfikator entailment/NLI albo ostroznie zaprojektowany drugi model, ale to jest osobny temat.

Kontrprzyklad granicy guard:

```text
claim: Quiz 2 trwa 30 minut.
source_id: D1_current_quiz_scope
quote: Quiz 2 obejmuje dokladnie dwa tematy: petle `while` oraz list comprehensions.
```

Taki output moze przejsc czesc checkow mechanicznych: zrodlo istnieje, a cytat wystepuje w zrodle. Nadal pozostaje problem: cytat dotyczy tematow quizu, a `claim` dotyczy czasu trwania. Guard nie rozstrzyga tu automatycznie relacji znaczeniowej.

W Labie 3 kod sprawdza, czy output jest wystarczajaco ustrukturyzowany i formalnie spojny, aby w ogole dalo sie go dalej oceniac. Reczny raport sprawdza wybrane przypadki i wskazuje, gdzie mechaniczny guard pomaga, a gdzie nadal potrzebny jest osad czlowieka.

## 8. Zwiazek Z Labem 2

Lab 2 pokazywal, ze jakosc odpowiedzi zalezy od tego, jaki kontekst system pokazuje modelowi. Lab 3 pokazuje kolejny krok: nawet gdy kontekst zostal wybrany, output modelu nadal trzeba sprawdzic przed uzyciem.

To laczy sie z pojeciem groundedness, czyli pytaniem, czy odpowiedz rzeczywiscie wynika ze zrodel. Output guard nie jest pelna automatyczna ocena groundedness. Jest jedna z warstw potrzebnych w takim systemie.

## 9. Najwazniejsza Intuicja

Model nie powinien byc traktowany jak zwykla funkcja, ktorej wynik mozna bez sprawdzenia przekazac dalej. W systemie GenAI output modelu jest danymi wejsciowymi dla kolejnego komponentu. Takie dane trzeba parsowac, walidowac, laczyc z trace'em i dopiero potem decydowac, czy wolno je pokazac uzytkownikowi albo przekazac dalej.
