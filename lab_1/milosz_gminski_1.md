# Raport do Labu 1

## 0. Jak oceniać różnicę

Różnicę między `v0` i `v1` oceniam najpierw po typie zmiany, a dopiero potem po tym, czy odpowiedź wygląda lepiej stylistycznie. Sama lista punktowana, krótszy tekst albo bardziej profesjonalny ton nie są wystarczającym dowodem poprawy.

Mocniejszym dowodem jest to, że `v1` lepiej wykonało konkretne polecenie, nie zgadywało brakujących informacji albo wyraźnie pokazało ograniczenia odpowiedzi.

## 1. Mapa przypadków

| ID przypadku | Ocena | Typ różnicy | Efekt | Najkrótszy dowód |
| --- | --- | --- | --- | --- |
| `c1_beginner_explanation` | `niejasne` | `jakość merytoryczna` | `niejasne` | `v0` wyjaśnia samowywołanie funkcji i ma prosty przykład liczenia do 5. `v1` jest krótsze, ale przykład ze schodkami bardziej przypomina zwykłe liczenie/mnożenie niż rekurencję. |
| `c2_brief_comparison` | `bez zmian` | `format` | `głównie forma` | Obie wersje wyjaśniają LIFO/FIFO i podają analogię. `v1` jest bardziej uporządkowane, ale nie daje wyraźnie lepszego rozumienia niż `v0`. |
| `c3_self_check_mode` | `bez zmian` | `wykonanie polecenia` | `bez zmian` | Obie wersje mają dokładnie 3 pytania i tylko pytania. Jawne sprawdzenia przechodzą w `v0` i `v1`, więc sam kontrakt nie daje tu mocnej przewagi. |
| `c4_course_uncertainty` | `lepsze` | `bezpieczeństwo / uczciwość` | `realna poprawa` | `v0` też mówi, że nie zna quizu, ale `v1` robi to krócej i jaśniej: nie ma dostępu do informacji o kursie, a potem podaje dokładnie 2 rzeczy do sprawdzenia. |
| `c5_feedback_mode` | `lepsze` | `wykonanie polecenia` | `realna poprawa` | `v0` dodaje wstęp, kodowy przykład i szersze wyjaśnienie. `v1` zostaje przy dokładnie 2 punktach: jedna rzecz poprawna i jedna do poprawy. |
| `c6_personalized_plan_limit` | `lepsze` | `ograniczenie systemu` | `realna poprawa` | `v0` zakłada np. 1-2 godziny dziennie i podstawowe tematy. `v1` nie udaje pełnej personalizacji, podaje ogólne sugestie i wskazuje brakujące dane. |

## 2. Najmocniejsze dowody poprawy

### Poprawa 1

- `case_id:` `c5_feedback_mode`
- `typ różnicy:` `wykonanie polecenia`
- `efekt:` `realna poprawa`
- `dowód z v0:` `v0` zaczyna od wstępu: "Oto moja ocena Twojego wyjaśnienia", a potem dodaje długi przykład z funkcją `add(x, y)`.
- `dowód z v1:` `v1` daje dokładnie dwa punkty: jeden o tym, co poprawne, i jeden o tym, że parametr to wartość przekazywana do funkcji, a nie wartość zwracana.
- `reguła kontraktu, która mogła zadziałać:` "Jeśli użytkownik prosi o konkretną strukturę, liczbę elementów albo typ outputu, spełnij to zanim dodasz dodatkową pomoc."
- `dlaczego to jest realna poprawa, a nie tylko format:` Użytkownik prosił o feedback dokładnie w 2 punktach, a nie o miniwykład. `v1` lepiej utrzymało tryb zadania.
- `czego ten dowód jeszcze nie pokazuje:` Nie pokazuje, że każda przyszła korekta merytoryczna będzie pełna i najlepsza dydaktycznie.

### Poprawa 2

- `case_id:` `c6_personalized_plan_limit`
- `typ różnicy:` `ograniczenie systemu`
- `efekt:` `realna poprawa`
- `dowód z v0:` `v0` przyjmuje założenia, np. około 1-2 godziny dziennie oraz podstawowe tematy z programowania.
- `dowód z v1:` `v1` zaczyna od informacji, że do spersonalizowanego planu potrzebuje więcej danych, a potem wypisuje termin egzaminu, słabe tematy i dostępny czas.
- `reguła kontraktu, która mogła zadziałać:` "Jeśli prośba zależy od informacji, których faktycznie nie masz, powiedz to jasno i wskaż studentowi, co sprawdzić albo jakich informacji brakuje."
- `dlaczego to jest realna poprawa, a nie tylko format:` Zmienia się zachowanie systemu: `v1` mniej udaje personalizację i wyraźniej oddziela ogólne sugestie od danych potrzebnych do prawdziwego planu.
- `czego ten dowód jeszcze nie pokazuje:` Nie pokazuje, że system potrafi później ułożyć dobry plan po otrzymaniu danych.

## 3. Najważniejsze ograniczenie

- `case_id:` `c1_beginner_explanation`
- `typ różnicy:` ograniczenie systemu
- `dowód z v0:` `v0` mówi, że rekurencja oznacza, że funkcja wywołuje sama siebie, i pokazuje liczenie do 5 przez kolejne wywołania.
- `dowód z v1:` `v1` ma krótszą formę, ale przykład ze schodkami nie pokazuje wyraźnie samowywołania ani warunku stopu.
- `co kontrakt poprawił, jeśli cokolwiek poprawił:` Ograniczył długość odpowiedzi i utrzymał poziom dla początkującego.
- `czego kontrakt nadal nie rozwiązuje:` Sam kontrakt nie gwarantuje, że przykład będzie merytorycznie trafny.
- `jaka warstwa kontroli byłaby potrzebna dalej:` dodatkowa weryfikacja

## 4. Odrzucone słabsze wyjaśnienie

- `słabsze wyjaśnienie:` `v1 jest lepsze, bo jest krótsze`
- `case_id:` `c1_beginner_explanation`
- `typ różnicy:` `jakość merytoryczna`
- `dowód przeciw temu wyjaśnieniu:` `v1` jest krótsze, ale przykład ze schodkami nie pokazuje dobrze mechanizmu rekurencji.
- `lepsze wyjaśnienie na podstawie dowodu:` Krótsza odpowiedź nie wystarczy. Trzeba sprawdzić, czy przykład faktycznie pomaga zrozumieć pojęcie. W tym przypadku przewaga `v1` jest niejasna.

## 5. Werdykt

- `werdykt:` `v1 trochę pomogło`
- `najmocniejszy dowód z case_id:` `c5_feedback_mode`
- `najważniejsze ograniczenie z case_id:` `c1_beginner_explanation`
- `krótkie uzasadnienie werdyktu:` `v1` realnie pomaga w pilnowaniu trybu, liczby elementów i brakujących danych, szczególnie w feedbacku i personalizacji. Nie wystarcza jednak do zapewnienia trafności przykładu merytorycznego.

## 6. Ograniczona zmiana

- `edytowany plik:` `src/versions/v1_task_contract/task_contract.txt`
- `docelowe case_id:` `c1_beginner_explanation`
- `typ różnicy, którą zmiana miała poprawić:` `jakość merytoryczna`
- `jednozdaniowy opis zmiany:` Dodałem regułę, że przykład ma pokazywać dokładnie wyjaśniane pojęcie, a nie tylko luźno podobną sytuację.
- `dowód przed zmianą:` `v1` podało przykład schodków, w którym liczenie kondygnacji i mnożenie nie pokazywało jasno rekurencji.
- `dowód po zmianie:` Po zmianie `v1` nadal użyło przykładu schodów, ale dopisało, że problem jest dzielony na mniejsze problemy liczenia kroków na jednej kondygnacji.
- `ocena zmiany:` niejasne
- `dlaczego to jest realna poprawa, kosmetyka albo regres:` Zmiana trochę przesunęła odpowiedź w stronę wyjaśnianego pojęcia, ale przykład nadal nie pokazuje jasno samowywołania ani warunku stopu. Dowód jest więc za słaby, żeby uznać to za realną poprawę.

## 7. Czego te wyniki jeszcze nie dowodzą

- Nie dowodzą, że `v1` zawsze będzie merytorycznie lepsze od `v0`.
- Nie dowodzą, że jawne sprawdzenia wystarczą do oceny jakości odpowiedzi.
- Nie dowodzą, że kontrakt zadania zastępuje kontekst kursu albo weryfikację faktów.
- Nie dowodzą, że pojedyncze uruchomienie modelu daje stabilny wynik dla wszystkich prób.
