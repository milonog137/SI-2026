# Raport Do Labu 3

Imie i nazwisko: `<imie nazwisko>`

Wypelniaj ten raport po kolei, w trakcie pracy. Kazda sekcja odpowiada jednemu krokowi z [opis_zadania.md](./opis_zadania.md).

Kazdy wazny wniosek powinien wskazywac konkretny dowod z:

- terminala,
- `make test`,
- `src/app/output_guard.py`,
- `outputs/traces/*.json`,
- `outputs/checks/*.md`,
- `src/sources/*.md`.

## 1. Start I Srodowisko

Wypelnic po Kroku 1.

- `katalog pracy:` `<np. zadania/lab_3/src>`
- `wynik make doctor:` `<local files: ok / failed + krotki opis>`
- `GROQ_API_KEY:` `<present / missing>`
- `czy byl problem srodowiskowy:` `<nie / tak + co naprawiono albo czego brakuje>`

Krotka notatka:

```text
<1-3 zdania tylko jesli cos bylo istotne dla dalszej pracy>
```

## 2. Baseline

Wypelnic po pierwszym `make test`, przed naprawa `output_guard.py`.

Krotki wynik terminala:

```text
<wkleic krotki wynik, np. liczbe testow i liczbe failures>
```

| Failing test | Jaki zly output albo decyzje aplikacji ten test zatrzymuje | Co obecny guard robi zle |
| --- | --- | --- |
| `test_missing_required_field_fails` | Output bez wymaganego pola, np. bez `answer` albo `next_action`, nie moze byc traktowany jak poprawny kontrakt. | Guard przepuszcza niepelny output zamiast sprawdzic wszystkie pola wymagane przez kontrakt. |
| `test_unknown_status_fails` | `<jaki zly output albo decyzje aplikacji ten test zatrzymuje>` | `<co obecny guard robi zle>` |
| `test_unknown_next_action_fails` | `<jaki zly output albo decyzje aplikacji ten test zatrzymuje>` | `<co obecny guard robi zle>` |
| `test_source_id_must_exist_in_catalog` | `<jaki zly output albo decyzje aplikacji ten test zatrzymuje>` | `<co obecny guard robi zle>` |
| `test_source_id_must_be_in_context_not_only_in_catalog` | `<jaki zly output albo decyzje aplikacji ten test zatrzymuje>` | `<co obecny guard robi zle>` |
| `test_quote_must_be_exact_fragment_of_cited_source` | `<jaki zly output albo decyzje aplikacji ten test zatrzymuje>` | `<co obecny guard robi zle>` |
| `test_unsupported_answer_cannot_be_sent_as_normal_answer` | `<jaki zly output albo decyzje aplikacji ten test zatrzymuje>` | `<co obecny guard robi zle>` |

- `liczba testow failing przed naprawa:` `<liczba>`
- `czy to byl blad srodowiska:` `<tak / nie + uzasadnienie>`
- `co baseline pokazuje o wadliwej warstwie guard:` `<1-3 zdania: jaki wspolny wzorzec laczy te failingi>`

## 3. Audyt I Naprawa Guard

Wypelnic po doprowadzeniu `make test` do przejscia.

| Check / funkcja | Co bylo bledne w kodzie | Co poprawiono | Jaki ryzykowny output jest teraz zatrzymywany |
| --- | --- | --- | --- |
| `validate_required_fields` | `<bledne zalozenie>` | `<minimalna poprawka>` | `<ryzyko>` |
| `validate_enums` | `<bledne zalozenie>` | `<minimalna poprawka>` | `<ryzyko>` |
| `validate_evidence_sources` | `<bledne zalozenie>` | `<minimalna poprawka>` | `<ryzyko>` |
| `validate_quotes` | `<bledne zalozenie>` | `<minimalna poprawka>` | `<ryzyko>` |
| `validate_action_policy` | `<bledne zalozenie>` | `<minimalna poprawka>` | `<ryzyko>` |

- `wynik make test po naprawie:` `<np. OK, 8 tests passed>`
- `czy zmieniono testy:` `<nie / jesli tak, dlaczego>`
- `czy zmieniono dane wejsciowe, zrodla albo kontrakt przed Krokiem 4:` `<nie / jesli tak, dlaczego>`

### 3A. Zmieniony Kod Guard

Wkleic finalny kod potrzebny do oceny naprawy guard.

Wkleic:

- cale finalne wersje funkcji z `src/app/output_guard.py`, ktore zmieniono w Kroku 3,
- kazdy nowy helper, jesli zostal dodany,
- bez testow, trace'ow i niezmienionych plikow.

- `plik:` `src/app/output_guard.py`
- `wklejony zakres:` `<nazwy zmienionych funkcji albo zakres linii>`

```python
<wkleic finalny kod zmienionych funkcji z src/app/output_guard.py>
```

Krotki komentarz:

```text
<1-3 zdania: dlaczego wklejone fragmenty pokazuja wykonana naprawe>
```

## 4. Live Run

Wypelniac po kazdej parze `make ask` + `make check`.

| Case | Artefakty | Status | Next action | Guard / key check | Decyzja aplikacji |
| --- | --- | --- | --- | --- | --- |
| `c1_supported_quiz_scope` | `outputs/traces/c1_supported_quiz_scope.json` + `outputs/checks/c1_supported_quiz_scope.md` | `supported -> supported` | `answer_user` | `PASS + brak` | `pokazac answer, bo status, akcja i evidence przeszly checki guard.` |
| `c2_unsupported_quiz_duration` | `<trace + check>` | `unsupported -> <status>` | `<next_action>` | `<PASS / ATTENTION + check_id albo brak>` | `<pokazac / zatrzymac / doprecyzowac + 1 zdanie>` |
| `c3_partial_week3_recovery` | `<trace + check>` | `partial -> <status>` | `<next_action>` | `<PASS / ATTENTION + check_id albo brak>` | `<pokazac / zatrzymac / doprecyzowac + 1 zdanie>` |
| `c6_prompt_injection_pressure` | `<trace + check>` | `supported -> <status>` | `<next_action>` | `<PASS / ATTENTION + check_id albo brak>` | `<pokazac / zatrzymac / doprecyzowac + 1 zdanie>` |

Po wypelnieniu czterech wierszy:

- `najbardziej pouczajacy case:` `<case_id + dlaczego>`
- `czy aplikacja moglaby bezpiecznie pokazac wszystkie answer:` `<tak / nie + uzasadnienie>`

## 5. Analiza Wybranego Trace

Wypelnic po wybraniu jednego case'a do glebszej analizy.

- `wybrany case:` `<case_id>`
- `dlaczego ten case:` `<1-2 zdania>`

| Element trace/check/source | Najwazniejszy fragment albo obserwacja |
| --- | --- |
| `full_model_input` | `<co model dostal: pytanie, zrodla, istotna instrukcja>` |
| `raw_model_output` | `<najwazniejszy fragment surowego outputu>` |
| `parsed_output.status` | `<wartosc + komentarz>` |
| `parsed_output.risk_flags` | `<wartosc + komentarz>` |
| `parsed_output.next_action` | `<wartosc + komentarz>` |
| `evidence` | `<claim -> source_id -> quote + reczna ocena, czy quote wspiera claim>` |
| `output guard` | `<najwazniejszy passed/failed check + znaczenie>` |
| `src/sources` | `<czy zrodlo rzeczywiscie wspiera odpowiedz albo gdzie jest ograniczenie>` |

Decyzja aplikacji po analizie:

```text
<pokazac answer / poprosic o doprecyzowanie / odmowic / zatrzymac output / wymagac dodatkowej kontroli>
```

Uzasadnienie:

```text
<2-5 zdan opartych na trace, check report i zrodlach>
```

## 6. Propozycja Malej Interwencji

Wypelnic po analizie jednego trace. W tym kroku nie zmieniac juz plikow; zapisac tylko konkretna propozycje.

- `obserwacja:` `<co dokladnie zauwazono w trace/check/source>`
- `problem dla aplikacji:` `<dlaczego to przeszkadza w bezpiecznym uzyciu outputu>`
- `proponowana interwencja:` `<output_contract.md / output_guard.py + konkretna zmiana>`
- `oczekiwany efekt:` `<co powinno byc inne, gdyby sprawdzic propozycje w osobnym eksperymencie>`
- `czy to daje gwarancje, czy tylko zwieksza szanse:` `<1-2 zdania>`

## 7. Wniosek Koncowy

Odpowiedziec konkretnie:

1. `Co oznacza zdanie: output modelu jest niezaufanymi danymi?`

   `<2-4 zdania na podstawie wykonanego labu>`

2. `Co pokazala petla: uruchomienie pipeline -> analiza trace/check/source -> decyzja aplikacji -> propozycja interwencji?`

   `<2-4 zdania na podstawie live run, analizy trace i ograniczen guard>`

## Opcjonalnie: Transfer Na Innym Przypadku

Ta sekcja nie jest wymagana. Wypelnic tylko po zakonczeniu glownej petli labu, jesli wykonano dodatkowa skrocona analize drugiego przypadku.

- `drugi wybrany case:` `<case_id>`
- `co bylo podejrzane albo pouczajace:` `<1-2 zdania>`
- `konkretny dowod:` `<fragment trace / check report / zrodla>`
- `czy problem jest podobny do glownego przypadku, czy inny:` `<podobny / inny + dlaczego>`
- `jaka mala zmiane mozna byloby rozwazyc jako osobny eksperyment:` `<output_contract.md / output_guard.py + opis>`
- `dlaczego to nie musi byc ta sama zmiana co w glownej propozycji:` `<1-3 zdania>`
