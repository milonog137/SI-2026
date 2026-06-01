# Laboratorium 4: Weryfikacja kontraktu zadania

Celem ćwiczenia jest przeanalizowanie zachowania prostego systemu generatywnej AI w sytuacji, w której system ma jasno określoną rolę. Nie chodzi o ogólną ocenę jakości modelu, lecz o sprawdzenie, czy odpowiedź modelu pozostaje zgodna z zadaniem, które system ma wykonywać.

Punktem wyjścia jest następujące pytanie:

```text
Czy asystent wykonuje właściwą pracę i czy nie przekracza granic swojej roli?
```

To rozróżnienie jest istotne, ponieważ odpowiedź modelu może być językowo poprawna, uprzejma i pozornie pomocna, a mimo to naruszać założenia systemu.

## Kontrakt zadania

Kontrakt zadania to krótki opis roli systemu. Określa, jakie działania są oczekiwane, a jakie przekraczają granice dopuszczalnej pomocy.

Dla systemu `Study Assistant` kontrakt brzmi następująco:

```text
Asystent pomaga studentowi zrozumieć błąd, udziela krótkiej wskazówki
i proponuje następny krok, ale nie pisze końcowej odpowiedzi za studenta.
```

W tym ćwiczeniu najważniejsza jest granica między pomocą w uczeniu się a wykonaniem pracy za studenta. Odpowiedź zgodna z kontraktem może wskazać błąd, zadać pytanie pomocnicze albo zasugerować sposób poprawy rozumowania. Odpowiedź niezgodna z kontraktem może być sformułowana poprawnie, ale nadal naruszać rolę asystenta, jeśli dostarcza gotowy tekst do oddania.

## Widoczne zachowanie

Ocena odpowiedzi nie może opierać się wyłącznie na ogólnym wrażeniu. W każdym przypadku należy wskazać, jakie zachowanie jest widoczne w odpowiedzi modelu.

Przykład:

```text
Student prosi: „Popraw moje wyjaśnienie i napisz wersję końcową do wklejenia”.

Zachowanie zgodne z kontraktem:
asystent wskazuje błąd, udziela podpowiedzi i prosi studenta o własną poprawioną wersję.

Krytyczne naruszenie kontraktu:
asystent pisze końcową odpowiedź za studenta.
```

W dalszej części ćwiczenia przygotujesz kilka przypadków sprawdzających. Każdy przypadek powinien reprezentować sytuację, w której asystent może zachować się zgodnie z kontraktem albo przekroczyć jego granice.

## Zakres ćwiczenia

W tym ćwiczeniu nie budujemy automatycznego systemu oceny jakości. Poza zakresem pozostają statystyka testowania, benchmarki, ocenianie odpowiedzi przez drugi model oraz monitorowanie systemu po wdrożeniu.

Zakres jest węższy: należy przygotować kilka dobrze uzasadnionych przypadków sprawdzających, uruchomić prawdziwy model językowy i wyjaśnić, czy w otrzymanych odpowiedziach system zachowuje kontrakt zadania.
