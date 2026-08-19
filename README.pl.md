# GhostMEAN

<p align="center">
  <img src="ghostmean/assets/icon.png" alt="GhostMEAN logo" width="220">
</p>

<p align="center"><em>🇬🇧 <a href="README.md">English version</a></em></p>

**Mean Aerodynamic Chord Calculator** — open source, Linux/Debian, bez
konta, bez chmury, bez subskrypcji. Twoje skrzydło, Twoja geometria, Twoje
dane — nic nie wychodzi poza Twój komputer.

## Opis pól i wyników (co jest czym)

### Panele skrzydła

Skrzydło to do 5 kolejnych paneli (od nasady do końcówki), każdy
zdefiniowany czterema liczbami. Program rysuje **jedną połówkę** i
automatycznie odbija ją lustrzanie na drugą stronę — zawsze zakładamy
skrzydło symetryczne.

| Pole | Znaczenie |
|---|---|
| `✓ / ✗ Panel N` | Włącza/wyłącza panel. Wyłączony panel zachowuje swoje wartości (nie zerują się), tylko nie wchodzi do obliczeń — możesz go z powrotem włączyć bez przepisywania liczb. |
| `Major` | Cięciwa nasadowa (większa) tego panelu — szerokość skrzydła w punkcie, gdzie panel się zaczyna (bliżej osi symetrii). |
| `Minor` | Cięciwa końcowa (mniejsza) tego panelu — szerokość w punkcie, gdzie panel się kończy (dalej od osi symetrii). |
| `Długość` | Rozpiętość TEGO panelu, mierzona wzdłuż osi rozpiętości (prostopadle do osi symetrii), **jednej strony** — nie całego skrzydła. |
| `Skos (LE)` | Skos krawędzi natarcia tego panelu. **Definicja zablokowana i zweryfikowana testami** (patrz niżej). |

**Skos (LE) — dokładna definicja:**
- Mierzony względem **globalnej osi rozpiętości** (prostopadłej do osi
  symetrii kadłuba), **absolutnie i niezależnie dla każdego panelu** — kąty
  się NIE kumulują między panelami. Panel 3 ze skosem 10° jest zawsze pod
  10° od osi rozpiętości, niezależnie od tego, jaki skos mają panele 1 i 2.
- `0°` = krawędź natarcia równoległa do osi rozpiętości.
- Dodatnia/ujemna wartość przesuwa krawędź natarcia w bok (w stronę
  krawędzi spływu / w stronę nosa).
- **Cięciwa się nie obraca** — zawsze zostaje prostopadła do globalnej osi
  rozpiętości, równoległa do cięciwy nasadowej. Skos przesuwa tylko
  krawędź natarcia; krawędź spływu wychodzi automatycznie (LE + lokalna
  cięciwa w danym miejscu), więc przy zwężeniu jej efektywny skos różni
  się od skosu LE — to prawidłowe, nie błąd.

### Jednostki

Przełącznik `mm` / `in` u góry przelicza WSZYSTKIE pola paneli na żywo
(nic nie trzeba wpisywać ponownie). Wewnątrz programu wszystko liczone
jest w mm — jednostka wyświetlania to tylko warstwa prezentacji.

### Wyniki

| Wynik | Znaczenie |
|---|---|
| `ROZPIĘTOŚĆ (WING SPAN)` | Całkowita rozpiętość, obie strony (suma długości wszystkich włączonych paneli × 2). |
| `POWIERZCHNIA (AREA)` | Całkowita powierzchnia, obie strony. |
| `WYDŁUŻENIE (ASPECT RATIO)` | span² / powierzchnia. |
| `M.A.C.` | Średnia cięciwa aerodynamiczna — liczona przez całkowanie rzeczywistego rozkładu cięciwy po całej rozpiętości (nie tylko wzorem dla jednego trapezu), więc wieloczłonowe skrzydła o różnym zwężeniu w każdym panelu liczą się poprawnie. |
| `MAC POSITION` — `X` | Pozycja krawędzi natarcia M.A.C., mierzona od krawędzi natarcia nasady (środka skrzydła). |
| `MAC POSITION` — `Y` | Pozycja M.A.C. wzdłuż rozpiętości, mierzona od osi symetrii. |
| `CG 25% / 28% / 30%` | Trzy najczęściej używane w modelarstwie punkty wyważenia. Wartość to odległość **od krawędzi natarcia, mierzona na stacji MAC** (czyli dokładnie to, co mierzysz linijką na fizycznym skrzydle w miejscu, gdzie wypada M.A.C.) — nie jest to współrzędna globalna. |
| `CG (NIESTANDARDOWY %)` | To samo, ale dla procentu, który sam ustawisz w polu `CG — własny %:` u góry. Program nie proponuje tej wartości sam — to Ty decydujesz, jaki dodatkowy poziom % chcesz zobaczyć. |

### Podgląd (widok z góry)

| Element | Wygląd |
|---|---|
| Obrys skrzydła | Jasnoniebieskie linie — krawędź natarcia, krawędź spływu, nasada, końcówki, obie strony. |
| Oś symetrii | Cienka przerywana linia pionowa na środku — przypomina, że to zawsze jedna geometria odbita lustrzanie. |
| Numery paneli | Małe cyfry `1`, `2`, ... przy krawędzi natarcia każdego panelu, po obu stronach. |
| Linia M.A.C. | Pomarańczowa przerywana linia pionowa w miejscu, gdzie wypada średnia cięciwa aerodynamiczna. |
| Znaczniki CG | Zielone krzyżyki na linii M.A.C., jeden na każdy poziom (25% / 28% / 30% / niestandardowy). Podpisy procentowe są celowo rozsunięte w pionowy stosik z cienką linią odniesienia do właściwego krzyżyka — przy typowych wartościach (25–30%) punkty leżą bardzo blisko siebie i bez tego zabiegu etykiety by się zlewały. |
| Wymiar rozpiętości | Pozioma linia z „wąsami” pod skrzydłem, z podpisem całkowitej rozpiętości w aktualnie wybranej jednostce. |

### Menu Plik

| Akcja | Skrót | Co robi |
|---|---|---|
| `Wczytaj dane (CSV)...` | Ctrl+O | Wczytuje wszystkie 5 paneli (także wyłączone), jednostkę i `CG — własny %` z pliku CSV. |
| `Zapisz dane (CSV)...` | Ctrl+S | Zapisuje to samo. Dane w pliku są zawsze w mm (niezależnie od jednostki wyświetlania), więc plik jest przenośny; jednostka wyświetlania też jest zapamiętana i przywracana przy wczytaniu. |
| `Eksportuj PDF (model)...` | Ctrl+P | Drukowalny arkusz A4 (jasne tło, ciemny tusz) z planem skrzydła i tabelą wyników — ta sama geometria co na ekranie. |

Nazwa pliku jest zapamiętywana między zapisem CSV a eksportem PDF — po
zapisaniu `skrzydlo.csv` okno eksportu PDF domyślnie zaproponuje
`skrzydlo.pdf`, żeby nazwy projektu zostały spójne.

## Historia zmian

### v0.3.1

- etykieta wyniku `CG (WŁASNY %)` → `CG (NIESTANDARDOWY %)` (i analogicznie w PDF: `(własny)` → `(niestandardowy)`) — "własny" sugerowało, że to punkt podany wprost przez użytkownika, podczas gdy to po prostu dodatkowy, ustawialny poziom procentowy. Pole wejściowe `CG — własny %:` zostaje bez zmian (tam faktycznie wpisujesz wartość sam)

### v0.3.0

- **Sweep — jednoznacznie zablokowana definicja** (potwierdzona i zweryfikowana testami geometrycznymi): skos KRAWĘDZI NATARCIA (LE) danego panelu, mierzony względem globalnej osi rozpiętości, ABSOLUTNIE i niezależnie dla każdego panelu (bez kumulowania kątów względem poprzedniego panelu). `0°` = LE równoległa do osi rozpiętości. Cięciwa pozostaje prostopadła do globalnej osi rozpiętości — skos przesuwa tylko LE w bok. Opisane wprost w `geometry.py` (docstring modułu) i w tooltipie pola „Skos (LE)” w GUI
- **CG zamiast samego AC**: `Procent MAC dla AC` zastąpiony przez `CG — własny %` + trzy stałe wyniki **CG 25% / CG 28% / CG 30%** plus **CG (własny %)** — każdy jako odległość od krawędzi natarcia mierzona na stacji MAC (czyli dokładnie to, co się mierzy linijką na skrzydle)
- **MAC POSITION** pokazuje teraz X i Y (X = pozycja krawędzi natarcia MAC od nasady) — przydatne przy własnych obliczeniach CG
- **Podgląd rozbudowany**: oś symetrii (przerywana linia środkowa), numeracja paneli (1, 2, ... przy każdym panelu, po obu stronach), wymiar całkowitej rozpiętości pod skrzydłem, oraz 4 znaczniki CG (25/28/30/własny%) na linii MAC z czytelnymi, rozsuniętymi etykietami (linie odniesienia łączą etykietę z właściwym znacznikiem, żeby bliskie procentowo punkty się nie zlewały)
- rysowanie geometrii nadal w 100% współdzielone między ekranem a PDF (`drawing.py`), więc eksport PDF ma te same elementy (oś symetrii, numery paneli, wymiar, znaczniki CG) w wersji drukowalnej

### v0.2.1

- jednoznacznie zdefiniowano `Sweep`: to skos KRAWĘDZI NATARCIA (LE) danego panelu, mierzony względem osi rozpiętości, niezależnie dla każdego panelu (nie względem poprzedniego panelu); cięciwa nie obraca się — skos przesuwa tylko LE w bok. Etykieta w UI zmieniona na `Skos (LE):`, pełny opis w tooltipie
- wyniki `MAC POSITION` pokazują teraz też `X` (pozycja krawędzi natarcia MAC od nasady), nie tylko `Y` — przyda się do obliczeń CG

### v0.2.0

- **Zapisz dane (CSV)** / **Wczytaj dane (CSV)** (menu Plik, Ctrl+S / Ctrl+O): zapisuje wszystkie 5 paneli (włącznie z wyłączonymi, żeby nic się nie gubiło), procent MAC dla AC i jednostki. Dane zapisywane kanonicznie w mm niezależnie od aktualnie wybranej jednostki w GUI, więc plik jest przenośny; jednostka wyświetlania też jest zapamiętywana i przywracana. Zweryfikowano pełny round-trip (zapis → wyzerowanie GUI → wczytanie → identyczne wartości i identyczny wynik M.A.C.)
- **Eksportuj PDF (model)** (menu Plik, Ctrl+P): drukowalny arkusz A4 (jasne tło, ciemny tusz — niezależnie od ciemnego motywu ekranu) z planem skrzydła z góry (ta sama geometria co podgląd na ekranie, wspólny moduł `drawing.py`) i tabelą wyników
- nazwa pliku zapamiętywana między zapisem CSV a eksportem PDF — po `save/skrzydlo.csv` okno zapisu PDF domyślnie proponuje `skrzydlo.pdf`, żeby nazwy zostały spójne

### v0.1.3

- checkbox panelu miał niewidoczny natywny wskaźnik na ciemnym tle — zastąpiono go czytelnym tekstowym znacznikiem: `✓ Panel N` (niebieski, pogrubiony) gdy panel włączony, `✗ Panel N` (czerwony, pogrubiony) gdy wyłączony; natywny box ukryty (`QCheckBox::indicator { width: 0; height: 0; }`), żeby nie dublował się ze znacznikiem tekstowym

### v0.1.2

- naprawiono mylące wrażenie, że panele 2–5 "nie działają": logika była poprawna (checkbox faktycznie włączał pola), ale wyłączone pola wyglądały niemal identycznie jak włączone, więc próba wpisania wartości bez zaznaczenia checkboxa wyglądała jak brak reakcji — dodano wyraźny styl `:disabled` (przyciemnione tło, wyszarzony tekst) oraz tooltip "Zaznacz checkbox „Panel N”, aby edytować ten panel"

### v0.1.1

- podgląd skrzydła wykorzystuje teraz pełną wysokość panelu (wcześniej trzymał się sztywnego minimum, zostawiając puste miejsce)
- `Dł.` → `Długość` w wierszu panelu
- wyniki przeprojektowane w stylu „Ghost”: podpisy wielkimi literami, wartości mono-fontem, `MAC POSITION` (Y) i `AERODYNAMIC CENTER` (X, Y) w osobnych, czytelnych liniach
- zweryfikowane na rzeczywistym dwupanelowym skrzydle (różne cięciwa i skos na każdym panelu) — wyniki MAC/pozycja MAC/AC zgodne z ręcznym przeliczeniem wzorów co do 3–4 miejsca po przecinku; obliczenia (`geometry.py`) niezmienione

### v0.1.0 — pierwsza wersja

- do 5 paneli skrzydła (każdy: włącz/wyłącz, Major Chord, Minor Chord,
  Panel Length, Sweep +/−)
- jednostki mm lub cale (przełączane w locie, wartości przeliczane)
- automatycznie liczone:
  - Wing Span (rozpiętość)
  - Area (powierzchnia)
  - Aspect Ratio (wydłużenie)
  - M.A.C. (średnia cięciwa aerodynamiczna) — liczona przez **całkowanie
    rzeczywistego rozkładu cięciwy**, nie tylko wzorem dla jednego
    trapezu, więc wieloczłonowe skrzydła o różnym zwężeniu w każdym
    panelu liczą się poprawnie
  - pozycja M.A.C. (rozpiętościowo i wzdłuż cięciwy)
  - Aerodynamic Center przy zadanym % MAC (domyślnie 25%)
- graficzny podgląd skrzydła z góry (obie połówki, linia MAC, znacznik AC)

## Uruchomienie

```bash
pip install -e .
ghostmean-gui
```

albo bez instalacji:

```bash
pip install PySide6
python -m ghostmean
```

## Dostępność (accessibility)

Interfejs projektowany od razu z myślą o obsłudze jedną ręką i przy
słabszym wzroku:
- duże czcionki, wysoki kontrast (ciemny motyw, jasnoniebieskie akcenty)
- wszystkie kontrolki to spinboxy z klawiaturową obsługą (strzałki/scroll),
  żadna funkcja rdzenia nie wymaga precyzyjnego przeciągania myszą ani
  jednoczesnego wciskania kilku klawiszy
- etykiety accessibleName na kluczowych polach pod czytniki ekranu
- duże, czytelne liczby wyników

## Matematyka (skrót)

Dla panelu o cięciwie nasadowej `Cr`, cięciwie końcowej `Ct` i długości `L`:

```
MAC_panelu = (2/3) * Cr * (1+λ+λ²)/(1+λ),   λ = Ct/Cr
```

Dla całego (wieloczłonowego) skrzydła liczymy `MAC` oraz jego pozycję przez
całkowanie `c(y)²` i `c(y)·y` po rozpiętości — patrz komentarz w
`ghostmean/geometry.py`. Sprawdzone względem znanego przykładu referencyjnego
(11"/6" → MAC≈8.745") oraz przypadku skrzydła prostokątnego (MAC = stała
cięciwa).

## Plan na później

- symetria lewej/prawej połówki — na razie zawsze symetryczne (świadoma decyzja, patrz historia zmian v0.3.0); osobne panele L/P to potencjalna, większa przebudowa na przyszłość
- import geometrii z DXF/SVG (świadomie odłożone — dużo trudniejszy problem niż zapis/odczyt CSV, wymaga rozpoznania osi symetrii i granic paneli z dowolnego rysunku)
- pakiet Flatpak / AppImage (jak w GhostPoster)

## Licencja

MIT.
