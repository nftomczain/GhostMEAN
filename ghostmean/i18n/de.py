STRINGS = {
    "window_title": "GhostMEAN {version} — Mean Aerodynamic Chord Calculator",

    "menu_file": "Datei",
    "menu_new_project": "Neues Projekt...",
    "menu_load_csv": "Daten laden (CSV)...",
    "menu_save_csv": "Daten speichern (CSV)...",
    "menu_export_pdf": "PDF exportieren (Modell)...",
    "menu_export_stations": "Stationen exportieren (CSV)...",
    "menu_export_stations_tooltip": (
        "Separates Format: vollständige, aufgelöste Geometrie (Y/LE/TE/Flügeltiefe) an jeder Station — "
        "nicht zum erneuten Laden gedacht, nur zur Verwendung beim Bau"
    ),
    "menu_help": "Hilfe",
    "menu_wiki": "Wiki (Online-Dokumentation)",

    "new_project_title": "Neues Projekt",
    "new_project_body": (
        "Geometrie zurücksetzen?\n"
        "Alle Paneele werden auf die Ausgangswerte zurückgesetzt."
    ),
    "new_project_status": "Neues Projekt — Geometrie zurückgesetzt",

    "topbar_units": "Einheiten:",
    "topbar_units_accessible": "Einheitenauswahl",
    "topbar_cg_custom": "CG — eigener %:",
    "topbar_cg_custom_accessible": "Eigener Ziel-Prozentsatz MAC für CG",
    "topbar_show_dims": "Bemaßung in der Vorschau",
    "topbar_show_dims_accessible": "Paneelmaße in der Vorschau anzeigen",
    "topbar_language": "Sprache:",
    "topbar_language_accessible": "Auswahl der Oberflächensprache",

    "panels_box_title": "Flügelpaneele (bis zu 5)",
    "panel_label": "Panel {n}",
    "panel_enable_accessible": "Panel {n} aktivieren",
    "panel_major_label": "Major:",
    "panel_minor_label": "Minor:",
    "panel_length_label": "Länge:",
    "panel_sweep_label": "Pfeilung (LE):",
    "panel_major_name": "Hauptsehne",
    "panel_minor_name": "Endsehne",
    "panel_length_name": "Paneellänge",
    "panel_sweep_name": "Vorderkanten-Pfeilung (LE), bezogen auf die Spannweitenachse",
    "panel_disabled_hint": "\n\nAktivieren Sie das Kästchen „Panel N“, um dieses Panel zu bearbeiten",
    "panel_copy_tooltip": "Panel {a} → Panel {b} kopieren",
    "panel_copy_accessible": "Panel {a} in Panel {b} kopieren",
    "panel_copy_no_next_tooltip": "Kein nächstes Panel zum Kopieren",
    "panel_stations_tooltip": "Genaue Geometrie (Stationen) von Panel {n} anzeigen",
    "panel_stations_accessible": "Stationen von Panel {n} anzeigen",
    "panel_copied_status": "Panel {a} → Panel {b}: kopiert",

    "sweep_tooltip": (
        "Pfeilung der VORDERKANTE (Leading Edge) dieses Panels.\n"
        "Gemessen relativ zur Spannweitenachse (senkrecht zur Symmetrieachse),\n"
        "UNABHÄNGIG für jedes Panel — NICHT relativ zum vorherigen Panel.\n"
        "Die Flügeltiefe dreht sich nicht mit der Pfeilung — bleibt parallel\n"
        "zur Wurzeltiefe; die Pfeilung verschiebt nur die Vorderkante seitlich."
    ),

    "warn_major_le_zero": "Panel {n}: Major ≤ 0",
    "warn_minor_le_zero": "Panel {n}: Minor ≤ 0",
    "warn_length_le_zero": "Panel {n}: Länge ≤ 0",
    "warn_minor_gt_major": "Panel {n}: Minor > Major (ungewöhnliche Verjüngung)",
    "warn_large_sweep": "Panel {n}: große Pfeilung ({v:.0f}°) — Geometrie prüfen",
    "warn_discontinuity": (
        "Panel {b}: Major ({bm:.1f}mm) ≠ Minor von Panel {a} ({am:.1f}mm) — "
        "echter Sprung von {jump:+.1f}mm, sichtbar in der Zeichnung und im MAC"
    ),

    "results_title": "Ergebnisse",
    "results_span": "SPANNWEITE (WING SPAN)",
    "results_span_accessible": "Spannweite (Wing Span)",
    "results_area": "FLÄCHE (AREA)",
    "results_area_accessible": "Fläche (Area)",
    "results_ar": "STRECKUNG (ASPECT RATIO)",
    "results_ar_accessible": "Streckung (Aspect Ratio)",
    "results_mac": "M.A.C.",
    "results_mac_pos": "M.A.C.-POSITION",
    "results_mac_pos_accessible": "M.A.C.-Position — X von der Vorderkante der Wurzel, Y von der Symmetrieachse",
    "results_cg25": "CG 25%",
    "results_cg25_accessible": "CG bei 25% MAC, Abstand von der Vorderkante an der MAC-Station",
    "results_cg28": "CG 28%",
    "results_cg28_accessible": "CG bei 28% MAC, Abstand von der Vorderkante an der MAC-Station",
    "results_cg30": "CG 30%",
    "results_cg30_accessible": "CG bei 30% MAC, Abstand von der Vorderkante an der MAC-Station",
    "results_cg_custom": "CG (EIGENER %)",
    "results_cg_custom_accessible": "CG bei einem eigenen (frei gewählten) Prozentsatz MAC",

    "preview_title": "Vorschau (Draufsicht)",
    "preview_accessible": "Flügelvorschau (Draufsicht)",
    "preview_no_data": "Keine Paneeldaten",

    "stations_title": "Stationen",
    "stations_header_station": "Station",
    "stations_header_y": "Y",
    "stations_header_le": "LE",
    "stations_header_te": "TE",
    "stations_header_chord": "Flügeltiefe",
    "stations_accessible": "Flügelstationstabelle",
    "station_root": "Flügelwurzel",
    "station_tip": "Flügelspitze",
    "station_mid": "S{n}",
    "station_mid_end": "S{n} (Ende von P{n})",
    "station_mid_start": "S{n} (Anfang von P{p})",

    "default_project_name": "fluegel",
    "stations_filename_suffix": "_stationen",

    "dialog_save_csv_title": "Daten speichern (CSV)",
    "dialog_load_csv_title": "Daten laden (CSV)",
    "dialog_export_pdf_title": "PDF exportieren (Modell)",
    "dialog_export_stations_title": "Stationen exportieren (CSV)",
    "filter_csv": "CSV (*.csv)",
    "filter_pdf": "PDF (*.pdf)",

    "error_save_title": "Fehler beim Speichern",
    "error_load_title": "Fehler beim Laden",
    "error_export_title": "Fehler beim Exportieren",
    "no_geometry_title": "Keine Geometrie",
    "no_geometry_body": "Aktivieren Sie mindestens ein Panel, bevor Sie Stationen exportieren.",

    "status_saved": "Gespeichert: {path}",
    "status_loaded": "Geladen: {path}",
    "status_exported_pdf": "Exportiert: {path}",
    "status_exported_stations": "Stationen exportiert: {path}",

    "station_view_title_suffix": " — Stationen",
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
        "Dieses Panel ist deaktiviert — keine Geometrie.\n"
        "Aktivieren Sie das Kästchen, um es einzuschalten."
    ),

    "pdf_title": "GhostMEAN — Flügelmodell",
    "pdf_span": "Spannweite (Wing Span)",
    "pdf_area": "Fläche (Area)",
    "pdf_ar": "Streckung (Aspect Ratio)",
    "pdf_mac": "M.A.C.",
    "pdf_mac_x": "MAC — Position X",
    "pdf_mac_y": "MAC — Position Y",
    "pdf_cg25": "CG 25% MAC (von LE an der MAC-Station)",
    "pdf_cg28": "CG 28% MAC (von LE an der MAC-Station)",
    "pdf_cg30": "CG 30% MAC (von LE an der MAC-Station)",
    "pdf_cg_custom": "CG {pct:.0f}% MAC (eigener)",
    "menu_about": "Über",
    "about_window_title": "Über — GhostMEAN",
    "about_version_accessible": "Aktuelle Programmversion",
    "about_link_wiki_accessible": "Projekt-Wiki im Browser öffnen",
    "about_link_github_accessible": "GitHub-Repository im Browser öffnen",
    "about_link_support_accessible": "Projekt-Diskussionen auf GitHub im Browser öffnen",
    "about_close": "Schließen",
}
