STRINGS = {
    "window_title": "GhostMEAN — Mean Aerodynamic Chord Calculator",

    "menu_file": "Fichier",
    "menu_new_project": "Nouveau projet...",
    "menu_load_csv": "Charger les données (CSV)...",
    "menu_save_csv": "Enregistrer les données (CSV)...",
    "menu_export_pdf": "Exporter le PDF (modèle)...",
    "menu_export_stations": "Exporter les stations (CSV)...",
    "menu_export_stations_tooltip": (
        "Format séparé : géométrie complète et résolue (Y/LE/TE/corde) à chaque station — "
        "non destiné à être rechargé, uniquement pour la construction"
    ),

    "new_project_title": "Nouveau projet",
    "new_project_body": (
        "Effacer la géométrie ?\n"
        "Tous les panneaux seront réinitialisés à leurs valeurs de départ."
    ),
    "new_project_status": "Nouveau projet — géométrie réinitialisée",

    "topbar_units": "Unités :",
    "topbar_units_accessible": "Sélection des unités",
    "topbar_cg_custom": "CG — personnalisé %:",
    "topbar_cg_custom_accessible": "Pourcentage MAC personnalisé pour le CG",
    "topbar_show_dims": "Cotes dans l'aperçu",
    "topbar_show_dims_accessible": "Afficher les cotes des panneaux dans l'aperçu",
    "topbar_language": "Langue :",
    "topbar_language_accessible": "Sélection de la langue de l'interface",

    "panels_box_title": "Panneaux d'aile (jusqu'à 5)",
    "panel_label": "Panneau {n}",
    "panel_enable_accessible": "Activer le panneau {n}",
    "panel_major_label": "Major:",
    "panel_minor_label": "Minor:",
    "panel_length_label": "Longueur :",
    "panel_sweep_label": "Flèche (LE) :",
    "panel_major_name": "Corde amont",
    "panel_minor_name": "Corde aval",
    "panel_length_name": "Longueur du panneau",
    "panel_sweep_name": "Flèche du bord d'attaque (LE), par rapport à l'axe d'envergure",
    "panel_disabled_hint": "\n\nCochez la case « Panneau N » pour modifier ce panneau",
    "panel_copy_tooltip": "Copier le panneau {a} → panneau {b}",
    "panel_copy_accessible": "Copier le panneau {a} vers le panneau {b}",
    "panel_copy_no_next_tooltip": "Aucun panneau suivant à copier",
    "panel_stations_tooltip": "Afficher la géométrie exacte (stations) du panneau {n}",
    "panel_stations_accessible": "Afficher les stations du panneau {n}",
    "panel_copied_status": "Panneau {a} → Panneau {b} : copié",

    "sweep_tooltip": (
        "Flèche du BORD D'ATTAQUE (Leading Edge) de ce panneau.\n"
        "Mesurée par rapport à l'axe d'envergure (perpendiculaire à l'axe de symétrie),\n"
        "INDÉPENDAMMENT pour chaque panneau — PAS par rapport au panneau précédent.\n"
        "La corde ne tourne pas avec la flèche — elle reste parallèle à la\n"
        "corde d'emplanture ; la flèche ne décale que le bord d'attaque latéralement."
    ),

    "warn_major_le_zero": "Panneau {n} : Major ≤ 0",
    "warn_minor_le_zero": "Panneau {n} : Minor ≤ 0",
    "warn_length_le_zero": "Panneau {n} : Longueur ≤ 0",
    "warn_minor_gt_major": "Panneau {n} : Minor > Major (effilement inhabituel)",
    "warn_large_sweep": "Panneau {n} : flèche importante ({v:.0f}°) — vérifiez la géométrie",
    "warn_discontinuity": (
        "Panneau {b} : Major ({bm:.1f}mm) ≠ Minor du panneau {a} ({am:.1f}mm) — "
        "saut réel de {jump:+.1f}mm visible sur le dessin et dans le MAC"
    ),

    "results_title": "Résultats",
    "results_span": "ENVERGURE (WING SPAN)",
    "results_span_accessible": "Envergure (Wing Span)",
    "results_area": "SURFACE (AREA)",
    "results_area_accessible": "Surface (Area)",
    "results_ar": "ALLONGEMENT (ASPECT RATIO)",
    "results_ar_accessible": "Allongement (Aspect Ratio)",
    "results_mac": "M.A.C.",
    "results_mac_pos": "POSITION C.M.A.",
    "results_mac_pos_accessible": "Position de la C.M.A. — X depuis le bord d'attaque de l'emplanture, Y depuis l'axe de symétrie",
    "results_cg25": "CG 25%",
    "results_cg25_accessible": "CG à 25% MAC, distance depuis le bord d'attaque à la station MAC",
    "results_cg28": "CG 28%",
    "results_cg28_accessible": "CG à 28% MAC, distance depuis le bord d'attaque à la station MAC",
    "results_cg30": "CG 30%",
    "results_cg30_accessible": "CG à 30% MAC, distance depuis le bord d'attaque à la station MAC",
    "results_cg_custom": "CG (PERSONNALISÉ %)",
    "results_cg_custom_accessible": "CG à un pourcentage MAC personnalisé (défini librement)",

    "preview_title": "Aperçu (vue de dessus)",
    "preview_accessible": "Aperçu de l'aile (vue de dessus)",
    "preview_no_data": "Aucune donnée de panneau",

    "stations_title": "Stations",
    "stations_header_station": "Station",
    "stations_header_y": "Y",
    "stations_header_le": "LE",
    "stations_header_te": "TE",
    "stations_header_chord": "Corde",
    "stations_accessible": "Tableau des stations de l'aile",
    "station_root": "Emplanture",
    "station_tip": "Saumon",
    "station_mid": "S{n}",
    "station_mid_end": "S{n} (fin de P{n})",
    "station_mid_start": "S{n} (début de P{p})",

    "default_project_name": "aile",
    "stations_filename_suffix": "_stations",

    "dialog_save_csv_title": "Enregistrer les données (CSV)",
    "dialog_load_csv_title": "Charger les données (CSV)",
    "dialog_export_pdf_title": "Exporter le PDF (modèle)",
    "dialog_export_stations_title": "Exporter les stations (CSV)",
    "filter_csv": "CSV (*.csv)",
    "filter_pdf": "PDF (*.pdf)",

    "error_save_title": "Erreur d'enregistrement",
    "error_load_title": "Erreur de chargement",
    "error_export_title": "Erreur d'exportation",
    "no_geometry_title": "Aucune géométrie",
    "no_geometry_body": "Activez au moins un panneau avant d'exporter les stations.",

    "status_saved": "Enregistré : {path}",
    "status_loaded": "Chargé : {path}",
    "status_exported_pdf": "Exporté : {path}",
    "status_exported_stations": "Stations exportées : {path}",

    "station_view_title_suffix": " — stations",
    "station_view_panel_title": "PANNEAU {n}",
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
        "Ce panneau est désactivé — pas de géométrie.\n"
        "Cochez la case pour l'activer."
    ),

    "pdf_title": "GhostMEAN — Modèle d'aile",
    "pdf_span": "Envergure (Wing Span)",
    "pdf_area": "Surface (Area)",
    "pdf_ar": "Allongement (Aspect Ratio)",
    "pdf_mac": "M.A.C.",
    "pdf_mac_x": "MAC — position X",
    "pdf_mac_y": "MAC — position Y",
    "pdf_cg25": "CG 25% MAC (depuis LE à la station MAC)",
    "pdf_cg28": "CG 28% MAC (depuis LE à la station MAC)",
    "pdf_cg30": "CG 30% MAC (depuis LE à la station MAC)",
    "pdf_cg_custom": "CG {pct:.0f}% MAC (personnalisé)",
}
