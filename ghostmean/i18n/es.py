STRINGS = {
    "window_title": "GhostMEAN {version} — Mean Aerodynamic Chord Calculator",

    "menu_file": "Archivo",
    "menu_new_project": "Nuevo proyecto...",
    "menu_load_csv": "Cargar datos (CSV)...",
    "menu_save_csv": "Guardar datos (CSV)...",
    "menu_export_pdf": "Exportar PDF (modelo)...",
    "menu_export_stations": "Exportar estaciones (CSV)...",
    "menu_export_stations_tooltip": (
        "Formato separado: geometría completa y resuelta (Y/LE/TE/cuerda) en cada estación — "
        "no está pensado para volver a cargarse, solo para usarse en la construcción"
    ),
    "menu_help": "Ayuda",
    "menu_wiki": "Wiki (documentación en línea)",

    "new_project_title": "Nuevo proyecto",
    "new_project_body": (
        "¿Borrar la geometría?\n"
        "Todos los paneles se restablecerán a sus valores iniciales."
    ),
    "new_project_status": "Nuevo proyecto — geometría restablecida",

    "topbar_units": "Unidades:",
    "topbar_units_accessible": "Selección de unidades",
    "topbar_cg_custom": "CG — personalizado %:",
    "topbar_cg_custom_accessible": "Porcentaje MAC personalizado para el CG",
    "topbar_show_dims": "Dimensiones en la vista previa",
    "topbar_show_dims_accessible": "Mostrar las dimensiones de los paneles en la vista previa",
    "topbar_language": "Idioma:",
    "topbar_language_accessible": "Selección del idioma de la interfaz",

    "panels_box_title": "Paneles del ala (hasta 5)",
    "panel_label": "Panel {n}",
    "panel_enable_accessible": "Activar panel {n}",
    "panel_major_label": "Mayor:",
    "panel_minor_label": "Menor:",
    "panel_length_label": "Longitud:",
    "panel_sweep_label": "Flecha (LE):",
    "panel_major_name": "Cuerda mayor",
    "panel_minor_name": "Cuerda menor",
    "panel_length_name": "Longitud del panel",
    "panel_sweep_name": "Flecha del borde de ataque (LE), respecto al eje de envergadura",
    "panel_disabled_hint": "\n\nMarque la casilla «Panel N» para editar este panel",
    "panel_copy_tooltip": "Copiar panel {a} → panel {b}",
    "panel_copy_accessible": "Copiar panel {a} al panel {b}",
    "panel_copy_no_next_tooltip": "No hay panel siguiente que copiar",
    "panel_stations_tooltip": "Mostrar la geometría exacta (estaciones) del panel {n}",
    "panel_stations_accessible": "Mostrar estaciones del panel {n}",
    "panel_copied_status": "Panel {a} → Panel {b}: copiado",

    "sweep_tooltip": (
        "Flecha del BORDE DE ATAQUE (Leading Edge) de este panel.\n"
        "Medida respecto al eje de envergadura (perpendicular al eje de simetría),\n"
        "DE FORMA INDEPENDIENTE para cada panel — NO respecto al panel anterior.\n"
        "La cuerda no gira con la flecha — permanece paralela a la cuerda\n"
        "de raíz; la flecha solo desplaza lateralmente el borde de ataque."
    ),

    "warn_major_le_zero": "Panel {n}: Mayor ≤ 0",
    "warn_minor_le_zero": "Panel {n}: Menor ≤ 0",
    "warn_length_le_zero": "Panel {n}: Longitud ≤ 0",
    "warn_minor_gt_major": "Panel {n}: Menor > Mayor (estrechamiento inusual)",
    "warn_large_sweep": "Panel {n}: flecha grande ({v:.0f}°) — revise la geometría",
    "warn_discontinuity": (
        "Panel {b}: Mayor ({bm:.1f}mm) ≠ Menor del panel {a} ({am:.1f}mm) — "
        "salto real de {jump:+.1f}mm visible en el dibujo y en el MAC"
    ),

    "results_title": "Resultados",
    "results_span": "ENVERGADURA (WING SPAN)",
    "results_span_accessible": "Envergadura (Wing Span)",
    "results_area": "SUPERFICIE (AREA)",
    "results_area_accessible": "Superficie (Area)",
    "results_ar": "ALARGAMIENTO (ASPECT RATIO)",
    "results_ar_accessible": "Alargamiento (Aspect Ratio)",
    "results_mac": "M.A.C.",
    "results_mac_pos": "POSICIÓN DE C.M.A.",
    "results_mac_pos_accessible": "Posición de la C.M.A. — X desde el borde de ataque de la raíz, Y desde el eje de simetría",
    "results_cg25": "CG 25%",
    "results_cg25_accessible": "CG al 25% MAC, distancia desde el borde de ataque en la estación MAC",
    "results_cg28": "CG 28%",
    "results_cg28_accessible": "CG al 28% MAC, distancia desde el borde de ataque en la estación MAC",
    "results_cg30": "CG 30%",
    "results_cg30_accessible": "CG al 30% MAC, distancia desde el borde de ataque en la estación MAC",
    "results_cg_custom": "CG (PERSONALIZADO %)",
    "results_cg_custom_accessible": "CG en un porcentaje MAC personalizado (definido libremente)",

    "preview_title": "Vista previa (vista superior)",
    "preview_accessible": "Vista previa del ala (vista superior)",
    "preview_no_data": "Sin datos del panel",

    "stations_title": "Estaciones",
    "stations_header_station": "Estación",
    "stations_header_y": "Y",
    "stations_header_le": "LE",
    "stations_header_te": "TE",
    "stations_header_chord": "Cuerda",
    "stations_accessible": "Tabla de estaciones del ala",
    "station_root": "Raíz",
    "station_tip": "Punta del ala",
    "station_mid": "S{n}",
    "station_mid_end": "S{n} (fin de P{n})",
    "station_mid_start": "S{n} (inicio de P{p})",

    "default_project_name": "ala",
    "stations_filename_suffix": "_estaciones",

    "dialog_save_csv_title": "Guardar datos (CSV)",
    "dialog_load_csv_title": "Cargar datos (CSV)",
    "dialog_export_pdf_title": "Exportar PDF (modelo)",
    "dialog_export_stations_title": "Exportar estaciones (CSV)",
    "filter_csv": "CSV (*.csv)",
    "filter_pdf": "PDF (*.pdf)",

    "error_save_title": "Error al guardar",
    "error_load_title": "Error al cargar",
    "error_export_title": "Error al exportar",
    "no_geometry_title": "Sin geometría",
    "no_geometry_body": "Active al menos un panel antes de exportar las estaciones.",

    "status_saved": "Guardado: {path}",
    "status_loaded": "Cargado: {path}",
    "status_exported_pdf": "Exportado: {path}",
    "status_exported_stations": "Estaciones exportadas: {path}",

    "station_view_title_suffix": " — estaciones",
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
        "Este panel está desactivado — sin geometría.\n"
        "Marque la casilla para activarlo."
    ),

    "pdf_title": "GhostMEAN — Modelo del ala",
    "pdf_span": "Envergadura (Wing Span)",
    "pdf_area": "Superficie (Area)",
    "pdf_ar": "Alargamiento (Aspect Ratio)",
    "pdf_mac": "M.A.C.",
    "pdf_mac_x": "MAC — posición X",
    "pdf_mac_y": "MAC — posición Y",
    "pdf_cg25": "CG 25% MAC (desde LE en la estación MAC)",
    "pdf_cg28": "CG 28% MAC (desde LE en la estación MAC)",
    "pdf_cg30": "CG 30% MAC (desde LE en la estación MAC)",
    "pdf_cg_custom": "CG {pct:.0f}% MAC (personalizado)",
    "menu_about": "Acerca de",
    "about_window_title": "Acerca de — GhostMEAN",
    "about_version_accessible": "Versión actual de la aplicación",
    "about_link_wiki_accessible": "Abrir la Wiki del proyecto en el navegador",
    "about_link_github_accessible": "Abrir el repositorio de GitHub en el navegador",
    "about_link_support_accessible": "Abrir las discusiones del proyecto en GitHub en el navegador",
    "about_close": "Cerrar",
}
