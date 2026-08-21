# GhostMEAN

<p align="center">
  <img src="ghostmean/assets/icon.png" alt="GhostMEAN logo" width="220">
</p>

<p align="center"><em>🇬🇧 <a href="README.md">English version</a></em></p>

<p align="center">
  <a href="https://github.com/nftomczain/GhostPoster/actions"><img alt="CI" src="https://img.shields.io/badge/CI-GitHub%20Actions-blue"></a>
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="Platform" src="https://img.shields.io/badge/Platform-Linux%20AppImage-46606c?logo=linux&logoColor=white">  
</p>


---
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
| `⧉` | Kopiuje ten panel do następnego: `Major` następnego panelu = `Minor` tego panelu (zachowana ciągłość cięciwy), `Minor`/`Długość`/`Skos` skopiowane jako punkt startowy do dalszej edycji. Następny panel zostaje automatycznie włączony. Niedostępny przy Panelu 5 (brak kolejnego panelu). |

**Walidacja (nieblokująca):** program na bieżąco sprawdza włączone panele i pokazuje ostrzeżenia pod tabelą paneli (nie blokuje obliczeń — to tylko sygnał, że coś wygląda nietypowo):
- `Major ≤ 0`, `Minor ≤ 0` lub `Długość ≤ 0`
- `Minor > Major` (nietypowe zwężenie — może być celowe, ale zwykle to pomyłka)
- duży skos (>60°) — warto sprawdzić, czy to zamierzone

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

### Język

Przełącznik `Język:` (prawy górny róg) zmienia interfejs na żywo, bez
restartu i bez utraty wpisanych danych — geometria, jednostki i wyniki
zostają dokładnie takie same. Dotyczy też eksportowanego PDF. Dostępne:
`pl`, `en`, `ru`, `es`, `de`, `fr`. Etykiety stacji też są tłumaczone
(nazwy nasady/końcówki/stacji pośrednich) — poza eksportem CSV stacji,
który świadomie zostaje w kanonicznych, polskich/ASCII-bezpiecznych
etykietach niezależnie od wybranego języka, bo to format wymiany danych
do budowy, nie zlokalizowany artefakt.

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

### Stacje (Station View) — v0.4.0

Skrzydło jest zbudowane z granic — **stacji**: nasada, granica po każdym panelu, końcówka. Dla każdej stacji program zna dokładnie: pozycję wzdłuż rozpiętości (Y), pozycję krawędzi natarcia (LE), pozycję krawędzi spływu (TE) i lokalną cięciwę.

- **Tabela „Stacje”** (pod podglądem) pokazuje to dla całego skrzydła naraz — jeden wiersz na stację (Nasada, S1, S2, ..., Końcówka).
- **Przycisk `📐` przy każdym panelu** otwiera dokładną geometrię TEGO panelu (Y START/END, LE START/END, TE START/END, CHORD START/END, SWEEP) — dokładnie te liczby, które potrzebujesz przy fizycznym budowaniu skrzydła z planu. Przy wyłączonym panelu pokazuje komunikat zamiast pustych danych.
- **Eksportuj stacje (CSV)** (menu Plik) — osobny, drugi format pliku: `station,y_mm,le_x_mm,te_x_mm,chord_mm`. To NIE jest plik projektu do wczytania z powrotem (do tego służy zwykły „Zapisz dane CSV”) — to gotowa, rozwiązana geometria do użycia przy budowie.

**Zasada GHOST MEAN (zablokowana, v0.4.0): dane użytkownika są prawdą — program nigdy nie "naprawia" geometrii za Ciebie.** Każdy panel jest rysowany dokładnie z własnego `Major` i `Minor`. Jeśli `Major` panelu N nie jest równe `Minor` panelu N-1 (nie zachowałeś ciągłości — np. nie użyłeś `⧉`), to NIE jest wygładzane: powstaje rzeczywisty, widoczny skok krawędzi spływu — dokładnie taki, jaki wynika z wpisanych liczb, identyczny na ekranie, w tabeli stacji i w PDF. Silnik MAC/Area i rysunek zawsze korzystają z tych samych, jednych danych źródłowych (`Panel data → stacje/LE/TE → rysunek → MAC/Area → PDF`) — nigdy nie mogą pokazać dwóch różnych geometrii. Program dodatkowo ostrzega o takiej niezgodności (`Major ≠ Minor panelu poprzedniego`), ale ostrzeżenie niczego nie blokuje.

### Podgląd (widok z góry)

| Element | Wygląd |
|---|---|
| Obrys skrzydła | Jasnoniebieskie linie — krawędź natarcia, krawędź spływu, nasada, końcówki, obie strony. |
| Oś symetrii | Cienka przerywana linia pionowa na środku — przypomina, że to zawsze jedna geometria odbita lustrzanie. |
| Numery paneli | Małe cyfry `1`, `2`, ... przy krawędzi natarcia każdego panelu, po obu stronach. |
| Linia M.A.C. | Pomarańczowa przerywana linia pionowa w miejscu, gdzie wypada średnia cięciwa aerodynamiczna. |
| Znaczniki CG | Zielone krzyżyki na linii M.A.C., jeden na każdy poziom (25% / 28% / 30% / niestandardowy). Podpisy procentowe są celowo rozsunięte w pionowy stosik z cienką linią odniesienia do właściwego krzyżyka — przy typowych wartościach (25–30%) punkty leżą bardzo blisko siebie i bez tego zabiegu etykiety by się zlewały. |
| Wymiar rozpiętości | Pozioma linia z „wąsami” pod skrzydłem, z podpisem całkowitej rozpiętości w aktualnie wybranej jednostce. |
| Wymiary paneli (opcjonalnie) | Włączane checkboxem `☑ Wymiary na podglądzie` u góry: linie ze strzałkami nad krawędzią natarcia (dzielą panele wzdłuż rozpiętości, bez tekstu — długość jest w legendzie), oraz czytelna lista pod skrzydłem, jedna linia na panel: `Panel 1:  250→200 \| 300mm \| 20°` — przydatne przy sprawdzaniu modelu odtwarzanego ze zdjęcia albo planu. |

### Menu Plik

| Akcja | Skrót | Co robi |
|---|---|---|
| `Nowy projekt...` | Ctrl+N | Po potwierdzeniu resetuje wszystkie 5 paneli do wartości początkowych (Panel 1 włączony, pozostałe wyłączone), `CG — własny %` do 25%, jednostkę do mm. |
| `Wczytaj dane (CSV)...` | Ctrl+O | Wczytuje wszystkie 5 paneli (także wyłączone), jednostkę i `CG — własny %` z pliku CSV. |
| `Zapisz dane (CSV)...` | Ctrl+S | Zapisuje to samo. Dane w pliku są zawsze w mm (niezależnie od jednostki wyświetlania), więc plik jest przenośny; jednostka wyświetlania też jest zapamiętana i przywracana przy wczytaniu. |
| `Eksportuj PDF (model)...` | Ctrl+P | Drukowalny arkusz A4 (jasne tło, ciemny tusz) z planem skrzydła i tabelą wyników — ta sama geometria co na ekranie. |
| `Eksportuj stacje (CSV)...` | — | Osobny format: pełna, rozwiązana geometria (Y/LE/TE/cięciwa) na każdej stacji — nie do wczytania z powrotem, tylko do użycia przy budowie. |

Nazwa pliku jest zapamiętywana między zapisem CSV a eksportem PDF — po
zapisaniu `skrzydlo.csv` okno eksportu PDF domyślnie zaproponuje
`skrzydlo.pdf`, żeby nazwy projektu zostały spójne. Katalog ostatnio
używanego pliku też jest zapamiętywany — `Ctrl+O` i kolejne zapisy/eksporty
domyślnie otwierają się w tym samym miejscu, w którym ostatnio pracowałeś.

## Historia zmian

### v0.4.10 — poprawka: niezadeklarowana zależność od Pillow

- **`scripts/build_appimage.sh` wymagał Pillow do przeskalowania ikony, ale nigdzie tego nie deklarował** — u mnie w środowisku testowym Pillow było zainstalowane z wcześniejszych, niepowiązanych zadań, więc problem umknął przy testach. Zgłoszone przez użytkownika: `ModuleNotFoundError: No module named 'PIL'` na czystym środowisku.
- Naprawione właściwie, nie łatą: zamiast auto-instalować Pillow (jak robimy dla `pyinstaller`), usunięto zależność całkowicie — przeskalowanie ikony teraz przez `PySide6.QtGui.QImage`, czyli bibliotekę, którą projekt i tak już wymaga (deklarowana w `pyproject.toml`). Zero nowych zależności.
- Zweryfikowane dosłownie: odinstalowałem Pillow z własnego środowiska (`pip uninstall pillow`), potwierdziłem `ModuleNotFoundError` przy próbie importu, uruchomiłem pełny build od zera — przechodzi, ikona zapisuje się poprawnie (256×256 PNG RGBA), zbudowany AppImage nadal się uruchamia.

### v0.4.9 — AppImage

- **`scripts/build_appimage.sh`** — buduje przenośny, jednoplikowy `.AppImage` (PyInstaller onedir → AppDir → appimagetool). Nie wymaga instalacji Pythona/Qt na maszynie uruchamiającej.
- Zabezpieczenia przeniesione wprost z GhostPostera, zanim jeszcze się ujawniły jako błędy tutaj: zawsze `chmod +x` na `appimagetool` niezależnie od tego, czy pobrany świeżo czy pozostawiony po przerwanym uruchomieniu; sanity-check ELF przed próbą uruchomienia (czytelny komunikat „usuń i spróbuj ponownie” zamiast kryptycznego błędu); usuwanie dołączonego `libxkbcommon(-x11).so*` przed pakowaniem, żeby AppImage korzystał z wersji systemowej (unika niezgodności ABI z natywnym stackiem X11/Wayland).
- **Realny bug znaleziony przy pierwszym uruchomieniu**: PyInstaller 6.x umieszcza biblioteki w podkatalogu `_internal/` (starsza konwencja `dist/ghostmean/*.so` już nie obowiązuje) — pierwsza wersja `AppRun` tego nie uwzględniała i binarka nie startowała (`cannot open shared object file`). Naprawione i zweryfikowane realnym uruchomieniem zbudowanego AppImage (`--appimage-extract-and-run`, bo w środowisku budowania brak FUSE).
- Przetestowane od zera trzy razy: świeży build, build z pozostawionym niewykonywalnym `appimagetool` (poprawnie ponownie `chmod +x`, bez zbędnego pobierania), build z celowo uszkodzonym plikiem `appimagetool` (poprawnie wykryty i pobrany na nowo).
- `packaging/*.desktop` + `*.metainfo.xml` dodane dla integracji z menu systemowym; poprawiona kategoria `.desktop` (jedna kategoria główna, bez ostrzeżenia `appimagetool`).

### v0.4.8 — RU, ES, DE, FR

Cztery kolejne języki, na bazie słownika terminów podanego przez użytkownika.

- **`ghostmean/i18n/ru.py`, `es.py`, `de.py`, `fr.py`** — po 117 kluczy każdy, zgodność z `pl.py` zweryfikowana programowo (identyczne zestawy kluczy I identyczne placeholdery `{...}` we wszystkich 6 plikach, zero rozjazdów). Terminologia lotnicza konsekwentna z podanym słownikiem: `MAC`, `CG`, `LE`, `TE`, `Sweep` zostają jako terminy techniczne we wszystkich językach; `Major`/`Minor` po rosyjsku zostają w angielskim zapisie (tak jak w praktyce branżowej), po hiszpańsku/niemiecku/francusku są tłumaczone (`Mayor/Menor`, `Hauptsehne/Endsehne`, `Corde amont/aval`).
- **Etykiety stacji też przetłumaczone** (`Nasada`→`Корень крыла`/`Raíz`/`Flügelwurzel`/`Emplanture` itd.) — wymagało to rozszerzenia `geometry.compute_stations()` o opcjonalny callback etykietujący (`label_fn`), żeby geometria dalej nie zależała od i18n, a UI mogło wstrzyknąć tłumaczenie. Domyślne zachowanie (bez `label_fn`) w 100% zgodne z poprzednią wersją — zweryfikowane regresją.
- **Eksport CSV stacji świadomie zostaje kanoniczny** (polskie, ASCII-bezpieczne etykiety) niezależnie od wybranego języka UI — to format wymiany danych do budowy, nie zlokalizowany artefakt (ta sama zasada co przy jednostkach w zwykłym CSV projektu).
- PDF przetestowany po rosyjsku — cyrylica renderuje się poprawnie, zero problemów z fontem.

### v0.4.7 — warstwa i18n (PL/EN)

Cały widoczny tekst interfejsu i eksportu PDF przeszedł przez wspólną warstwę tłumaczeń zamiast być zaszyty na sztywno w kodzie.

- **`ghostmean/i18n/`**: `pl.py` i `en.py`, każdy jeden płaski słownik `klucz → szablon` (112 kluczy, identyczny zestaw w obu plikach — sprawdzone programowo). Dodanie kolejnego języka to skopiowanie `pl.py`, przetłumaczenie wartości i dopisanie do `LANGUAGES` w `ghostmean/i18n/__init__.py` — reszta aplikacji nie wymaga zmian.
- **Przełącznik `Język:` w pasku górnym** — zmienia się na żywo, bez restartu, bez utraty wpisanych danych (zweryfikowane: MAC, geometria, CSV round-trip identyczne przed i po przełączeniu).
- Dotyczy menu, etykiet paneli, tooltipów, wyników, tabeli stacji, komunikatów walidacji, dialogów (Nowy projekt, Station View), pasków statusu — **oraz eksportu PDF** (tytuł, tabela wyników), który automatycznie używa aktualnie wybranego języka.
- **Świadoma granica zakresu**: etykiety stacji generowane w `geometry.compute_stations()` (`Nasada`/`Końcówka`/`S1`...) na razie zostają po polsku niezależnie od wybranego języka — podłączenie ich do i18n wymagałoby przekazania tłumaczenia do modułu geometrii, który dziś świadomie nie zależy od UI. Udokumentowane wprost w kodzie jako możliwy następny krok.

### v0.4.6

- Strzałki wymiarowe nad krawędzią natarcia (`☑ Wymiary na podglądzie`) straciły tekst z długością w mm — zostały same linie ze strzałkami, wizualnie dzielące panele wzdłuż rozpiętości. Dokładna długość jest już w legendzie pod skrzydłem (v0.4.2), więc nie trzeba jej powtarzać nad rysunkiem. Przy okazji zmniejszony górny margines (mniej pustego miejsca, skoro nie trzeba już rezerwować go na tekst).

### v0.4.5

- Cofnięte v0.4.4: `P1`–`P5` nad rysunkiem dublowało się z osobną numeracją paneli, która już jest zawsze widoczna bezpośrednio przy skrzydle. Wrócone do strzałek wymiarowych z długością w mm nad krawędzią natarcia — jedna numeracja (przy skrzydle), jedne wymiary (nad rysunkiem), bez powtórzeń.

### v0.4.4

- Górny rząd nad rysunkiem (przy `☑ Wymiary na podglądzie`) pokazuje teraz proste etykiety `P1`–`P5` zamiast strzałek wymiarowych z długością w mm — dokładne liczby są już w czytelnej legendzie pod skrzydłem (v0.4.2), więc górny rząd redukuje się do samego "co jest czym", bez powtarzania danych.

### v0.4.3 — realna skala zamiast auto-dopasowania

- **Skalowanie podglądu odwrócone**: wcześniej KAŻDE skrzydło (małe i duże) było skalowane, żeby maksymalnie wypełnić dostępne miejsce — więc na oko nie było widać, że jedno skrzydło jest małe, a drugie duże. Teraz skala jest stała (mm-na-piksel), skalibrowana na referencyjnym "dużym" skrzydle (2000mm rozpiętości / 350mm głębokości cięciwy): małe skrzydło realnie wygląda na małe (nie wypełnia okna), a im większe od punktu odniesienia, tym ciaśniej dopasowuje się do dostępnej przestrzeni (żeby nigdy nie wyjść poza ramkę). Dotyczy identycznie podglądu na ekranie i PDF (wspólny `drawing.py`).
- Przy okazji poprawiony niedokładny szacunek potrzebnej wysokości (było `mac_mm + max_chord`, teraz prawdziwy bounding-box głębokości liczony z rzeczywistych stacji).
- Geometria, obliczenia i tabela Stacje — nietknięte, to wyłącznie zmiana w renderze.

### v0.4.2 — dopieszczenie renderera wymiarów

Sam typografia, geometria i obliczenia nietknięte.

- **Etykiety paneli przestały się zlewać**: zamiast pojedynczej linii `Major→Minor | Długość | Skos°` upychanej pod krawędzią spływu każdego panelu (co przy 3+ panelach nachodziło na siebie w okolicy nasady), pod skrzydłem pojawia się teraz czytelna lista — jedna linia na panel, z jawnym numerem: `Panel 1:  250→200 | 300mm | 20°`, `Panel 2:  200→140 | 250mm | 10°`, itd. Numery paneli narysowane na skrzydle jednoznacznie wiążą listę z kształtem, więc nie trzeba zgadywać, który opis należy do której sekcji.
- **Naprawiony efekt uboczny znaleziony przy okazji**: górne strzałki wymiarowe (długość panelu) przy 4-5 krótkich panelach obok siebie potrafiły nałożyć się w nieczytelną papkę cyfr. Teraz etykieta długości po prostu nie rysuje się, gdy nie ma dla niej miejsca (strzałka zostaje) — czysto, zamiast śmieciowego tekstu.
- Górny rząd wymiarów (strzałki nad krawędzią natarcia) — bez zmian, jak było dobrze.

### v0.4.1

- **Scroll dla niższych rozdzielczości**: całe okno owinięte w `QScrollArea` (pionowo i poziomo, w razie potrzeby), więc żaden element UI nie jest już nieosiągalny na mniejszym ekranie — wcześniej okno miało sztywny rozmiar 1060×1040. Zweryfikowano: przy 1024×768 wszystko (łącznie z przyciskami `⧉`/`📐`) mieści się z samym pionowym scrollem; przy bardziej ekstremalnym 900×620 dochodzi też poziomy, bo panele mają swoją minimalną szerokość.
- Zweryfikowane wizualnie dokładnie to, o co prosił użytkownik: dialog `📐` dla Panelu 2 i Panelu 3 (na przykładzie 250→200→140→80 ze skosem), z potwierdzoną ciągłością — `Panel 3 Y START/LE START` dokładnie równe `Panel 2 Y END/LE END`.

### v0.4.0 — Station View

Pierwszy większy skok funkcjonalny od pierwszej wersji — pełna geometria stacji paneli, nie tylko MAC.

- **Tabela „Stacje”**: pod podglądem, jeden wiersz na każdą granicę panelu (Nasada, S1, S2, ..., Końcówka) — Y, LE, TE, cięciwa, na żywo w wybranej jednostce.
- **Przycisk `📐` przy każdym panelu**: dokładna geometria TEGO panelu (Y/LE/TE START i END, CHORD START i END, SWEEP) w osobnym oknie — dokładnie to, co potrzebne przy budowie fizycznego skrzydła z policzonego planu. Zweryfikowano na własnym przykładzie łańcuchowym użytkownika (250→200→140→80 przy długościach 300/250/200mm) — tabela stacji pokazuje Y=0/300/550/750mm i cięciwy 250/200/140/80mm, dokładnie zgodnie z wcześniej podaną tabelą.
- **Strzałki wymiarowe na podglądzie**: `☑ Wymiary na podglądzie` teraz rysuje też strzałkę z długością panelu nad krawędzią natarcia (nie tylko tekstowy podpis pod krawędzią spływu jak w v0.3.2).
- **Eksportuj stacje (CSV)**: drugi, niezależny format pliku (`station,y_mm,le_x_mm,te_x_mm,chord_mm`) — rozwiązana geometria do użycia przy budowie, nie plik projektu do wczytania z powrotem.
- **Realny bug znaleziony i naprawiony przy budowie tej funkcji** (nie tylko w Station View): silnik MAC/Area (`compute_wing_metrics`) zawsze liczył każdy panel z jego WŁASNYM `Major`, ale rysunek/tabela stacji od pierwszej wersji po cichu zakładały ciągłość (łączyły panele przez `Minor` poprzedniego, ignorując `Major` panelu bieżącego przy braku zgodności) — MAC i rysunek mogły więc pokazywać dwie różne geometrie. Nie ujawniło się wcześniej, bo we wszystkich dotychczasowych przykładach ciągłość była zachowana. **Naprawione właściwie, nie tylko ostrzeżeniem**: `geometry.compute_panel_stations()` liczy każdy panel z jego własnych danych (jedno źródło prawdy dla silnika i rysunku), a `geometry.compute_stations()` wykrywa niezgodność i wstawia dodatkowy punkt geometrii — realny, widoczny skok krawędzi spływu, identyczny na ekranie, w tabeli stacji i w PDF. Ostrzeżenie (`Major ≠ Minor panelu poprzedniego`) zostaje, ale niczego nie ukrywa ani nie blokuje.
- Świadomie pominięte w tej wersji (zgodnie z planem): DXF/SVG, profil/airfoil, twist, flaperony, niesymetryczne skrzydła, 3D.

### v0.3.3 — poprawki znalezione testem CSV

- **`Długość ≤ 0` było niewykrywalne**: pole `Długość` miało zakres `(0.01, 10000)`, więc `QDoubleSpinBox` automatycznie podnosił każdą wartość ≤0 (np. `0.0` z CSV) do `0.01` przed jakąkolwiek walidacją — ostrzeżenie nigdy się nie pojawiało. Naprawione: zakres zmieniony na `(0, 10000)`, zgodnie z `Major`/`Minor`, które już poprawnie pozwalały na 0 i polegały na walidacji, nie na clampowaniu. Zweryfikowane dokładnie na zgłoszonym przypadku (CSV z `Długość=0.000000`) — teraz poprawnie pokazuje `Panel N: Długość ≤ 0`, bez wpływu na stabilność obliczeń/PDF.
- **Checkbox „Wymiary na podglądzie” był niewidoczny**: globalny styl chowający natywny wskaźnik `QCheckBox` (patrz v0.1.3) dotyczy WSZYSTKICH checkboxów w aplikacji, ale tylko wiersze paneli miały własną kompensację (tekstowy `✓`/`✗`). Ten checkbox jej nie miał — był w pełni klikalny (potwierdzone), tylko bez żadnego widocznego stanu. Naprawione systemowo: wydzielona wspólna funkcja `style_toggle_checkbox()` używana teraz przez wszystkie checkboxy w aplikacji, żeby ten sam błąd nie wrócił przy kolejnych dodawanych przełącznikach.

### v0.3.2 — Quality of Life

- **Walidacja geometrii** (nieblokująca): ostrzeżenia pod tabelą paneli gdy `Major ≤ 0`, `Minor ≤ 0`, `Długość ≤ 0`, `Minor > Major` (nietypowe zwężenie) lub skos >60° (sprawdź, czy zamierzony). Obliczenia nadal działają — to tylko sygnał. Zweryfikowano, że skrajne/błędne dane (0, 0, 0.01mm, 89°) nie powodują wywalenia programu.
- **Wymiary na podglądzie**: nowy checkbox `☑ Wymiary na podglądzie` — pod krawędzią spływu każdego panelu pojawia się podpis `Major→Minor | Długość | Skos°`, przydatne przy odtwarzaniu modelu ze zdjęcia lub planu. Etykiety dynamicznie mierzone i dociskane do widocznego obszaru, żeby się nie przycinały przy panelach blisko krawędzi.
- **Kopiowanie panelu**: przycisk `⧉` przy każdym panelu (poza ostatnim) kopiuje go do następnego — `Minor` bieżącego panelu staje się `Major` następnego (zachowana ciągłość cięciwy), reszta pól skopiowana jako punkt startowy, następny panel automatycznie włączony. Pozwala budować wieloczłonowe skrzydło bez przepisywania wspólnych wartości.
- **Plik → Nowy projekt** (Ctrl+N): z potwierdzeniem, resetuje wszystkie 5 paneli, `CG — własny %` i jednostkę do stanu początkowego.
- **Zapamiętywanie ostatniego katalogu**: `Ctrl+O` oraz okna zapisu/eksportu domyślnie otwierają się w katalogu ostatnio używanego pliku.
- CG (25/28/30/niestandardowy) — bez zmian, zgodnie z planem.

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

### AppImage (Linux, bez instalacji Pythona)

```bash
./scripts/build_appimage.sh
./dist/GhostMEAN-<wersja>-x86_64.AppImage
```

Wymaga `pyinstaller` (skrypt sam go zainstaluje, jeśli brakuje) i `curl`
do pobrania `appimagetool` przy pierwszym budowaniu (potem cache w
`build/appimagetool.AppImage`). Wynikowy plik jest samodzielny — działa
na maszynie bez zainstalowanego Pythona czy Qt.

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

- **v0.5.0 — import DXF/SVG** (świadomie odłożone — dużo trudniejszy problem niż zapis/odczyt CSV, wymaga rozpoznania osi symetrii i granic paneli z dowolnego rysunku)
- **v0.6.0 — profil/airfoil**
- symetria lewej/prawej połówki — na razie zawsze symetryczne (świadoma decyzja, patrz historia zmian v0.3.0); osobne panele L/P to potencjalna, większa przebudowa na przyszłość
- pakiet Flatpak (AppImage już gotowy, patrz wyżej)

## Licencja

MIT.
