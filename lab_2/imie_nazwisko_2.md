# Raport do Labu 2

Raport wypełniać po wykonaniu przygotowania pojęciowego, `make doctor` i `make compare`. Odpowiedzi z przygotowania pojęciowego nie są osobną częścią raportu.

Wypełniać sekcje po kolei. Przypadek A i Przypadek B wymagają pełnej analizy. Szybka tabela obejmuje wszystkie cztery przypadki.

Pisać krótko. Nie opisywać wrażeń. Każdy ważny wniosek poprzeć konkretnym dowodem z:

- `src/outputs/compare.md`,
- `full_model_input`,
- odpowiedzi modelu,
- `selected_contexts.json`,
- `bad_contexts.json`,
- źródeł w `src/sources/`.

W tabelach `Wyniki Groq` w kolumnie `Dowód` wpisać krótki cytat albo konkretną obserwację z odpowiedzi modelu lub `full_model_input`.

Placeholdery w nawiasach ostrych, np. `<source_id>`, należy zastąpić własną treścią.

## 1. Przypadek A: `q1_quiz_scope`

- `pytanie użytkownika:` `<przepisać pytanie z questions.json>`
- `główny problem źródeł:` `<konflikt aktualne / stare / szum / prompt injection / inne + krótkie uzasadnienie>`
- `najlepszy wariant:` `<nazwa wariantu + 1 zdanie dlaczego>`
- `najbardziej ryzykowny wariant:` `<nazwa wariantu + 1 zdanie dlaczego>`

### Kontekst

Wpisać 1-2 najważniejsze użyte źródła.

| Użyte źródło | Dokładny fragment | Dlaczego użyte |
| --- | --- | --- |
| `<source_id>` | `<dokładny fragment ze źródła>` | `<aktualność / autorytet / relewantność / rozstrzyga konflikt>` |

Wpisać 1-3 źródła odrzucone albo ryzykowne.

| Odrzucone źródło | Dlaczego odrzucone | Typ problemu |
| --- | --- | --- |
| `<source_id>` | `<dlaczego nie powinno być podstawą odpowiedzi>` | `<stare / szum / sprzeczne / prompt injection / inne>` |

### Wyniki Groq

| Wariant | Najważniejszy wynik odpowiedzi | Dowód |
| --- | --- | --- |
| `no_context` | `<co model zrobił bez lokalnych danych>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |
| `all_context` | `<co model zrobił z wszystkimi źródłami>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |
| `selected_context` | `<co model zrobił z trafnym pakietem kontekstu>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |
| `selected_context_with_evidence_instruction` | `<co zmieniła instrukcja wskazywania źródeł>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |
| `bad_context` | `<co model zrobił z wadliwym pakietem kontekstu>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |

### Mapowanie dowodów

Wpisać 2-3 ważne stwierdzenia z odpowiedzi. Każde stwierdzenie połączyć z dokładnym źródłem i fragmentem.

| Stwierdzenie z odpowiedzi | Źródło | Dokładny fragment |
| --- | --- | --- |
| `<konkretna sprawdzalna informacja z odpowiedzi>` | `<source_id>` | `<dokładny fragment potwierdzający albo pokazujący brak podstawy>` |

### Osąd

- `dlaczego najlepszy wariant jest najlepszy:` `<wniosek + dowód z tabeli powyżej>`
- `co pogorszył albo pokazał najbardziej ryzykowny wariant:` `<wniosek + dowód>`
- `czego nadal nie wiadomo albo czego te wyniki nie dowodzą:` `<ograniczenie dowodu>`

## 2. Przypadek B: `q3_personalized_plan_limit`

- `pytanie użytkownika:` `<przepisać pytanie z questions.json>`
- `główny problem źródeł:` `<brak danych osobistych / szum / udawanie personalizacji / prompt injection / inne + krótkie uzasadnienie>`
- `najlepszy wariant:` `<nazwa wariantu + 1 zdanie dlaczego>`
- `najbardziej ryzykowny wariant:` `<nazwa wariantu + 1 zdanie dlaczego>`

### Kontekst

| Użyte źródło | Dokładny fragment | Dlaczego użyte |
| --- | --- | --- |
| `<source_id>` | `<dokładny fragment ze źródła>` | `<aktualność / autorytet / relewantność / pokazuje ograniczenie danych>` |

| Odrzucone źródło | Dlaczego odrzucone | Typ problemu |
| --- | --- | --- |
| `<source_id>` | `<dlaczego nie powinno być podstawą odpowiedzi>` | `<stare / szum / sprzeczne / prompt injection / inne>` |

### Wyniki Groq

| Wariant | Najważniejszy wynik odpowiedzi | Dowód |
| --- | --- | --- |
| `no_context` | `<co model zrobił bez lokalnych danych>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |
| `all_context` | `<co model zrobił z wszystkimi źródłami>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |
| `selected_context` | `<co model zrobił z trafnym pakietem kontekstu>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |
| `selected_context_with_evidence_instruction` | `<co zmieniła instrukcja wskazywania źródeł>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |
| `bad_context` | `<co model zrobił z wadliwym pakietem kontekstu>` | `<cytat albo obserwacja z odpowiedzi/full_model_input>` |

### Mapowanie dowodów

Wpisać 2-3 ważne stwierdzenia z odpowiedzi. Każde stwierdzenie połączyć z dokładnym źródłem i fragmentem.

| Stwierdzenie z odpowiedzi | Źródło | Dokładny fragment |
| --- | --- | --- |
| `<konkretna sprawdzalna informacja z odpowiedzi>` | `<source_id>` | `<dokładny fragment potwierdzający albo pokazujący brak podstawy>` |

### Osąd

- `dlaczego najlepszy wariant jest najlepszy:` `<wniosek + dowód z tabeli powyżej>`
- `co pogorszył albo pokazał najbardziej ryzykowny wariant:` `<wniosek + dowód>`
- `czego nadal nie wiadomo albo czego te wyniki nie dowodzą:` `<ograniczenie dowodu>`

## 3. Szybka Tabela Wszystkich Przypadków

Uzupełnić krótko. To nie ma być druga pełna analiza.

| ID przypadku | Najlepszy wariant | Najgorszy albo najbardziej ryzykowny wariant | Najważniejszy dowód | Główne ograniczenie |
| --- | --- | --- | --- | --- |
| `q1_quiz_scope` | `<wariant>` | `<wariant>` | `<krótki dowód>` | `<czego dowód nie rozstrzyga>` |
| `q2_week3_recovery` | `<wariant>` | `<wariant>` | `<krótki dowód>` | `<czego dowód nie rozstrzyga>` |
| `q3_personalized_plan_limit` | `<wariant>` | `<wariant>` | `<krótki dowód>` | `<czego dowód nie rozstrzyga>` |
| `q4_feedback_rules` | `<wariant>` | `<wariant>` | `<krótki dowód>` | `<czego dowód nie rozstrzyga>` |

## 4. Kontekst, Instrukcja, Odpowiedź

Odpowiedzieć na podstawie porównania `selected_context` i `selected_context_with_evidence_instruction`.

- `co zmienił sam kontekst w wariancie selected_context:` `<wniosek + question_id>`
- `co zmieniła dodatkowa instrukcja "odpowiadaj tylko na podstawie źródeł i wskazuj source_id" w wariancie selected_context_with_evidence_instruction:` `<wniosek + question_id>`
- `co nadal trzeba było sprawdzić w gotowej odpowiedzi:` `<co wymagało mapowania dowodów albo kontroli źródeł>`
- `jeden dowód z compare.md:` `<krótki cytat albo obserwacja>`

## 5. Ryzykowne Źródło

Użyć przykładu z `D7_prompt_injection` albo innego ryzykownego źródła.

- `source_id:` `<source_id>`
- `dokładny ryzykowny fragment:` `<cytat ze źródła>`
- `dlaczego ten fragment może wpłynąć na model i dlatego jest ryzykiem:` `<krótkie wyjaśnienie>`
- `co aplikacja używająca modelu powinna zrobić z tym źródłem:` `<użyć / odrzucić / użyć z ostrzeżeniem>`
- `uzasadnienie decyzji:` `<dowód z treści lub metadanych źródła>`

## 6. Odrzucone Słabsze Wyjaśnienie

Wybrać jedno kuszące, ale za słabe wyjaśnienie.

Przykłady:

- `selected_context jest lepszy, bo odpowiedź brzmi profesjonalniej`
- `all_context jest wadliwy, bo duża ilość kontekstu zawsze szkodzi`
- `model rozwiązał problem, bo podał source_id`
- `bad_context jest wadliwy tylko dlatego, że ma mniej źródeł`

Wypełnić:

- `słabsze wyjaśnienie:` `<wybrane wyjaśnienie, które brzmi kusząco, ale jest za słabe>`
- `question_id:` `<question_id>`
- `dowód przeciw temu wyjaśnieniu:` `<dowód z compare.md / full_model_input / źródeł / mapowania>`
- `lepsze wyjaśnienie oparte na danych, instrukcji albo mapowaniu dowodów:` `<lepszy wniosek>`

## 7. Werdykt Końcowy

Wpisać dokładnie jedną wartość:

- `trafny pakiet kontekstu wyraźnie pomógł`
- `trafny pakiet kontekstu częściowo pomógł`
- `instrukcja wskazywania źródeł była ważniejsza niż sam pakiet kontekstu`
- `na podstawie tych dowodów nie wiadomo`

Wypełnić:

- `werdykt:` `<jedna wartość z listy powyżej>`
- `najmocniejszy dowód z question_id:` `<question_id + dowód>`
- `najważniejsze ograniczenie tego dowodu:` `<czego ten dowód nie rozstrzyga>`
- `czego ten lab jeszcze nie dowodzi o automatycznym dostarczaniu kontekstu:` `<ograniczenie eksperymentu>`
