# Raport do Labu 1

Pisz krótko.

Zasada główna:

1. Najpierw nazwij typ różnicy między `v0` i `v1`.
2. Potem pokaż dowód z `v0` i `v1`.
3. Dopiero potem oceń, czy to realna poprawa, forma, regres, czy niejasne.

## 0. Jak oceniać różnicę

| Typ różnicy | Kiedy użyć |
| --- | --- |
| `format` | Odpowiedź jest krótsza, ma listę, ma mniej tekstu albo inny układ. |
| `wykonanie polecenia` | `v1` lepiej spełnia konkretną prośbę użytkownika, np. limit punktów, brak kodu, tylko pytania. |
| `bezpieczeństwo / uczciwość` | `v1` jawnie pokazuje brak danych, niepewność albo ryzyko zamiast zgadywać. |
| `jakość merytoryczna` | `v1` trafniej wyjaśnia pojęcie, lepiej diagnozuje błąd albo używa lepszego przykładu. |
| `ograniczenie systemu` | Przypadek pokazuje, czego sam kontrakt nadal nie rozwiązuje. |
| `niejasne` | Dowody nie pozwalają uczciwie rozstrzygnąć. |

| Typ różnicy | Siła dowodu |
| --- | --- |
| `format` | Słaby samodzielnie. Krótsza odpowiedź nie musi być lepsza. |
| `wykonanie polecenia` | Mocniejszy, jeśli pokazujesz konkretną prośbę i konkretną zmianę. |
| `bezpieczeństwo / uczciwość` | Mocny, jeśli `v1` przestaje zgadywać albo ujawnia brak danych. |
| `jakość merytoryczna` | Wymaga najwięcej uzasadnienia, bo jest najbardziej miękka. |
| `ograniczenie systemu` | Obowiązkowe, gdy kontrakt poprawił tylko część problemu. |

Nie wystarcza jako dowód:

- `v1 jest krótsze`
- `v1 brzmi lepiej`
- `v1 ma listę punktowaną`
- `jawne sprawdzenie przeszło`
- `model wykonał moją nową regułę`

To może być obserwacja pomocnicza, ale nie końcowy dowód.

## 1. Mapa przypadków

Używaj tylko tych wartości:

| Pole | Dozwolone wartości |
| --- | --- |
| `Ocena` | `lepsze`, `bez zmian`, `gorsze`, `niejasne` |
| `Typ różnicy` | `format`, `wykonanie polecenia`, `bezpieczeństwo / uczciwość`, `jakość merytoryczna`, `ograniczenie systemu`, `niejasne` |
| `Efekt` | `realna poprawa`, `głównie forma`, `regres`, `bez zmian`, `niejasne` |

Wypełnij tabelę dla wszystkich 6 przypadków.

| ID przypadku | Ocena | Typ różnicy | Efekt | Najkrótszy dowód |
| --- | --- | --- | --- | --- |
| `c1_beginner_explanation` |  |  |  |  |
| `c2_brief_comparison` |  |  |  |  |
| `c3_self_check_mode` |  |  |  |  |
| `c4_course_uncertainty` |  |  |  |  |
| `c5_feedback_mode` |  |  |  |  |
| `c6_personalized_plan_limit` |  |  |  |  |

## Mini przykład

To jest przykład demonstracyjny. Nie rozwiązuje żadnego z 6 przypadków z tego labu.

```text
case_id: demo_training_plan
ocena: lepsze
typ różnicy: bezpieczeństwo / uczciwość
efekt: realna poprawa

dowód z v0:
v0 od razu proponuje ćwiczenia: "zrób pompki, przysiady, deskę", mimo że nie zna zdrowia ani poziomu użytkownika.

dowód z v1:
v1 zaczyna od ograniczenia: "Jeśli masz ból pleców, kolan albo świeżą kontuzję..." i prosi o doprecyzowanie celu, poziomu i urazów.

reguła kontraktu, która mogła zadziałać:
"Jeśli brakuje informacji o zdrowiu lub poziomie zaawansowania, zaznacz to."

dlaczego to jest realna poprawa, a nie tylko format:
To nie jest tylko krótszy albo ładniej wypunktowany tekst. System przeszedł z generowania planu bez danych na ostrożną odpowiedź, która ujawnia ryzyko i brak informacji.

czego ten dowód jeszcze nie pokazuje:
Kontrakt nie sprawdza faktycznego stanu zdrowia użytkownika i nie weryfikuje, czy zaproponowane ćwiczenia są poprawne dla konkretnej osoby.
```

## 2. Najmocniejsze dowody poprawy

Wybierz dwa przypadki z najlepszym dowodem poprawy. Nie wybieraj przypadku tylko dlatego, że `v1` jest krótsze.

### Poprawa 1

- `case_id:`
- `typ różnicy:`
- `efekt:`
- `dowód z v0:`
- `dowód z v1:`
- `reguła kontraktu, która mogła zadziałać:`
- `dlaczego to jest realna poprawa, a nie tylko format:`
- `czego ten dowód jeszcze nie pokazuje:`

### Poprawa 2

- `case_id:`
- `typ różnicy:`
- `efekt:`
- `dowód z v0:`
- `dowód z v1:`
- `reguła kontraktu, która mogła zadziałać:`
- `dlaczego to jest realna poprawa, a nie tylko format:`
- `czego ten dowód jeszcze nie pokazuje:`

## 3. Najważniejsze ograniczenie

Wybierz jeden przypadek, który najlepiej pokazuje granicę kontraktu zadania.

- `case_id:`
- `typ różnicy:` ograniczenie systemu
- `dowód z v0:`
- `dowód z v1:`
- `co kontrakt poprawił, jeśli cokolwiek poprawił:`
- `czego kontrakt nadal nie rozwiązuje:`
- `jaka warstwa kontroli byłaby potrzebna dalej:` lepszy kontrakt zadania / więcej kontekstu / dodatkowa weryfikacja / wyraźniejsza granica narzędziowa / lepszy przebieg pracy albo stan

## 4. Odrzucone słabsze wyjaśnienie

Wybierz jedno kuszące, ale za słabe wyjaśnienie.

Przykłady:

- `v1 jest lepsze, bo jest krótsze`
- `v1 jest lepsze, bo ma listę`
- `v1 jest lepsze, bo test przeszedł`
- `v1 jest lepsze, bo brzmi bardziej profesjonalnie`

Wypełnij:

- `słabsze wyjaśnienie:`
- `case_id:`
- `typ różnicy:`
- `dowód przeciw temu wyjaśnieniu:`
- `lepsze wyjaśnienie na podstawie dowodu:`

## 5. Werdykt

Wpisz dokładnie jedną wartość:

- `v1 wyraźnie pomogło`
- `v1 trochę pomogło`
- `v1 jest głównie kosmetyczne`
- `na podstawie tych dowodów nie wiadomo`

Wypełnij:

- `werdykt:`
- `najmocniejszy dowód z case_id:`
- `najważniejsze ograniczenie z case_id:`
- `krótkie uzasadnienie werdyktu:`

## 6. Ograniczona zmiana

Zmień tylko `src/versions/v1_task_contract/task_contract.txt`.

Zmiana ma dotyczyć jednego problemu z mapy przypadków. Nie dodawaj losowej reguły tylko po to, żeby model ją wykonał.

- `edytowany plik:`
- `docelowe case_id:`
- `typ różnicy, którą zmiana miała poprawić:`
- `jednozdaniowy opis zmiany:`
- `dowód przed zmianą:`
- `dowód po zmianie:`
- `ocena zmiany:` pomogła / pogorszyła / głównie kosmetyczna / niejasne
- `dlaczego to jest realna poprawa, kosmetyka albo regres:`

## 7. Czego te wyniki jeszcze nie dowodzą

Wpisz 2-4 krótkie punkty.

- 
- 
- 
