STRINGS = {
    "window_title": "GhostMEAN {version} — Mean Aerodynamic Chord Calculator",

    "menu_file": "Plik",
    "menu_new_project": "Nowy projekt...",
    "menu_load_csv": "Wczytaj dane (CSV)...",
    "menu_save_csv": "Zapisz dane (CSV)...",
    "menu_export_pdf": "Eksportuj PDF (model)...",
    "menu_export_stations": "Eksportuj stacje (CSV)...",
    "menu_export_stations_tooltip": (
        "Osobny format: pełna, rozwiązana geometria (Y/LE/TE/cięciwa) na każdej stacji — "
        "nie do wczytania z powrotem, tylko do użycia przy budowie"
    ),
    "menu_help": "Pomoc",
    "menu_wiki": "Wiki (dokumentacja online)",

    "new_project_title": "Nowy projekt",
    "new_project_body": (
        "Wyczyścić geometrię?\n"
        "Wszystkie panele zostaną zresetowane do wartości początkowych."
    ),
    "new_project_status": "Nowy projekt — geometria zresetowana",

    "topbar_units": "Jednostki:",
    "topbar_units_accessible": "Wybór jednostek",
    "topbar_cg_custom": "CG — własny %:",
    "topbar_cg_custom_accessible": "Własny docelowy procent MAC dla CG",
    "topbar_show_dims": "Wymiary na podglądzie",
    "topbar_show_dims_accessible": "Pokaż wymiary paneli na podglądzie",
    "topbar_language": "Język:",
    "topbar_language_accessible": "Wybór języka interfejsu",

    "panels_box_title": "Panele skrzydła (do 5)",
    "panel_label": "Panel {n}",
    "panel_enable_accessible": "Włącz panel {n}",
    "panel_major_label": "Major:",
    "panel_minor_label": "Minor:",
    "panel_length_label": "Długość:",
    "panel_sweep_label": "Skos (LE):",
    "panel_major_name": "Cięciwa większa",
    "panel_minor_name": "Cięciwa mniejsza",
    "panel_length_name": "Długość panelu",
    "panel_sweep_name": "Skos krawędzi natarcia (LE), względem osi rozpiętości",
    "panel_disabled_hint": "\n\nZaznacz checkbox „Panel N”, aby edytować ten panel",
    "panel_copy_tooltip": "Kopiuj panel {a} → panel {b}",
    "panel_copy_accessible": "Kopiuj panel {a} do panelu {b}",
    "panel_copy_no_next_tooltip": "Brak kolejnego panelu do skopiowania",
    "panel_stations_tooltip": "Pokaż dokładną geometrię (stacje) panelu {n}",
    "panel_stations_accessible": "Pokaż stacje panelu {n}",
    "panel_copied_status": "Panel {a} → Panel {b}: skopiowano",

    "sweep_tooltip": (
        "Skos KRAWĘDZI NATARCIA (Leading Edge) tego panelu.\n"
        "Mierzony względem osi rozpiętości (prostopadłej do osi symetrii),\n"
        "NIEZALEŻNIE dla każdego panelu — NIE względem poprzedniego panelu.\n"
        "Cięciwa nie obraca się wraz ze skosem — zostaje równoległa do\n"
        "cięciwy nasadowej; skos przesuwa w bok tylko krawędź natarcia."
    ),

    "warn_major_le_zero": "Panel {n}: Major ≤ 0",
    "warn_minor_le_zero": "Panel {n}: Minor ≤ 0",
    "warn_length_le_zero": "Panel {n}: Długość ≤ 0",
    "warn_minor_gt_major": "Panel {n}: Minor > Major (nietypowe zwężenie)",
    "warn_large_sweep": "Panel {n}: duży skos ({v:.0f}°) — sprawdź geometrię",
    "warn_discontinuity": (
        "Panel {b}: Major ({bm:.1f}mm) ≠ Minor panelu {a} ({am:.1f}mm) — "
        "rzeczywisty skok {jump:+.1f}mm widoczny na rysunku i w MAC"
    ),

    "results_title": "Wyniki",
    "results_span": "ROZPIĘTOŚĆ (WING SPAN)",
    "results_span_accessible": "Rozpiętość (Wing Span)",
    "results_area": "POWIERZCHNIA (AREA)",
    "results_area_accessible": "Powierzchnia (Area)",
    "results_ar": "WYDŁUŻENIE (ASPECT RATIO)",
    "results_ar_accessible": "Wydłużenie (Aspect Ratio)",
    "results_mac": "M.A.C.",
    "results_mac_pos": "MAC POSITION",
    "results_mac_pos_accessible": "Pozycja M.A.C. — X od krawędzi natarcia nasady, Y od osi symetrii",
    "results_cg25": "CG 25%",
    "results_cg25_accessible": "CG przy 25% MAC, odległość od krawędzi natarcia na stacji MAC",
    "results_cg28": "CG 28%",
    "results_cg28_accessible": "CG przy 28% MAC, odległość od krawędzi natarcia na stacji MAC",
    "results_cg30": "CG 30%",
    "results_cg30_accessible": "CG przy 30% MAC, odległość od krawędzi natarcia na stacji MAC",
    "results_cg_custom": "CG (NIESTANDARDOWY %)",
    "results_cg_custom_accessible": "CG przy niestandardowym (dowolnie ustawionym) procencie MAC",

    "preview_title": "Podgląd (widok z góry)",
    "preview_accessible": "Podgląd skrzydła (widok z góry)",
    "preview_no_data": "Brak danych panelu",

    "stations_title": "Stacje",
    "stations_header_station": "Stacja",
    "stations_header_y": "Y",
    "stations_header_le": "LE",
    "stations_header_te": "TE",
    "stations_header_chord": "Cięciwa",
    "stations_accessible": "Tabela stacji skrzydła",
    "station_root": "Nasada",
    "station_tip": "Końcówka",
    "station_mid": "S{n}",
    "station_mid_end": "S{n} (koniec P{n})",
    "station_mid_start": "S{n} (start P{p})",

    "default_project_name": "skrzydlo",
    "stations_filename_suffix": "_stacje",

    "dialog_save_csv_title": "Zapisz dane (CSV)",
    "dialog_load_csv_title": "Wczytaj dane (CSV)",
    "dialog_export_pdf_title": "Eksportuj PDF (model)",
    "dialog_export_stations_title": "Eksportuj stacje (CSV)",
    "filter_csv": "CSV (*.csv)",
    "filter_pdf": "PDF (*.pdf)",

    "error_save_title": "Błąd zapisu",
    "error_load_title": "Błąd wczytywania",
    "error_export_title": "Błąd eksportu",
    "no_geometry_title": "Brak geometrii",
    "no_geometry_body": "Włącz przynajmniej jeden panel przed eksportem stacji.",

    "status_saved": "Zapisano: {path}",
    "status_loaded": "Wczytano: {path}",
    "status_exported_pdf": "Wyeksportowano: {path}",
    "status_exported_stations": "Wyeksportowano stacje: {path}",

    "station_view_title_suffix": " — stacje",
    "station_view_panel_title": "PANEL {n}",
    "station_view_y_start": "Y START",
    "station_view_y_end": "Y END",
    "station_view_le_start": "LE START",
    "station_view_le_end": "LE END",
    "station_view_te_start": "TE START",
    "station_view_te_end": "TE END",
    "station_view_chord_start": "CHORD START",
    "station_view_chord_end": "CHORD END",
    "station_view_sweep": "SWEEP (LE)",
    "station_view_disabled_body": (
        "Ten panel jest wyłączony — brak geometrii.\n"
        "Zaznacz checkbox, aby go włączyć."
    ),

    "pdf_title": "GhostMEAN — Model skrzydła",
    "pdf_span": "Rozpiętość (Wing Span)",
    "pdf_area": "Powierzchnia (Area)",
    "pdf_ar": "Wydłużenie (Aspect Ratio)",
    "pdf_mac": "M.A.C.",
    "pdf_mac_x": "MAC — pozycja X",
    "pdf_mac_y": "MAC — pozycja Y",
    "pdf_cg25": "CG 25% MAC (od LE na stacji MAC)",
    "pdf_cg28": "CG 28% MAC (od LE na stacji MAC)",
    "pdf_cg30": "CG 30% MAC (od LE na stacji MAC)",
    "pdf_cg_custom": "CG {pct:.0f}% MAC (niestandardowy)",
    "menu_about": "O programie",
    "about_window_title": "O programie — GhostMEAN",
    "about_version_accessible": "Aktualna wersja programu",
    "about_link_wiki_accessible": "Otwórz Wiki projektu w przeglądarce",
    "about_link_github_accessible": "Otwórz repozytorium na GitHubie w przeglądarce",
    "about_link_support_accessible": "Otwórz dyskusje projektu na GitHubie w przeglądarce",
    "about_close": "Zamknij",
}
