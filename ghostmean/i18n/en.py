STRINGS = {
    "window_title": "GhostMEAN {version} — Mean Aerodynamic Chord Calculator",

    "menu_file": "File",
    "menu_new_project": "New project...",
    "menu_load_csv": "Load data (CSV)...",
    "menu_save_csv": "Save data (CSV)...",
    "menu_export_pdf": "Export PDF (model)...",
    "menu_export_stations": "Export stations (CSV)...",
    "menu_export_stations_tooltip": (
        "A separate format: the fully-resolved geometry (Y/LE/TE/chord) at every station — "
        "not meant to be loaded back, only used for building"
    ),
    "menu_help": "Help",
    "menu_wiki": "Wiki (online documentation)",

    "new_project_title": "New project",
    "new_project_body": (
        "Clear the geometry?\n"
        "All panels will be reset to their initial values."
    ),
    "new_project_status": "New project — geometry reset",

    "topbar_units": "Units:",
    "topbar_units_accessible": "Unit selection",
    "topbar_cg_custom": "CG — custom %:",
    "topbar_cg_custom_accessible": "Custom target percent MAC for CG",
    "topbar_show_dims": "Dimensions on preview",
    "topbar_show_dims_accessible": "Show panel dimensions on the preview",
    "topbar_language": "Language:",
    "topbar_language_accessible": "Interface language selection",

    "panels_box_title": "Wing panels (up to 5)",
    "panel_label": "Panel {n}",
    "panel_enable_accessible": "Enable panel {n}",
    "panel_major_label": "Major:",
    "panel_minor_label": "Minor:",
    "panel_length_label": "Length:",
    "panel_sweep_label": "Sweep (LE):",
    "panel_major_name": "Major chord",
    "panel_minor_name": "Minor chord",
    "panel_length_name": "Panel length",
    "panel_sweep_name": "Leading-edge (LE) sweep, relative to the spanwise axis",
    "panel_disabled_hint": "\n\nCheck the \u201cPanel N\u201d checkbox to edit this panel",
    "panel_copy_tooltip": "Copy panel {a} → panel {b}",
    "panel_copy_accessible": "Copy panel {a} to panel {b}",
    "panel_copy_no_next_tooltip": "No next panel to copy into",
    "panel_stations_tooltip": "Show exact geometry (stations) for panel {n}",
    "panel_stations_accessible": "Show stations for panel {n}",
    "panel_copied_status": "Panel {a} → Panel {b}: copied",

    "sweep_tooltip": (
        "This panel's LEADING-EDGE sweep.\n"
        "Measured from the spanwise axis (perpendicular to the symmetry axis),\n"
        "INDEPENDENTLY for each panel — NOT relative to the previous panel.\n"
        "The chord does not rotate with the sweep — it stays parallel to the\n"
        "root chord; sweep only offsets the leading edge sideways."
    ),

    "warn_major_le_zero": "Panel {n}: Major ≤ 0",
    "warn_minor_le_zero": "Panel {n}: Minor ≤ 0",
    "warn_length_le_zero": "Panel {n}: Length ≤ 0",
    "warn_minor_gt_major": "Panel {n}: Minor > Major (unusual taper)",
    "warn_large_sweep": "Panel {n}: large sweep ({v:.0f}°) — double-check the geometry",
    "warn_discontinuity": (
        "Panel {b}: Major ({bm:.1f}mm) ≠ panel {a}'s Minor ({am:.1f}mm) — "
        "a real {jump:+.1f}mm step, visible in the drawing and in MAC"
    ),

    "results_title": "Results",
    "results_span": "WING SPAN",
    "results_span_accessible": "Wing Span",
    "results_area": "AREA",
    "results_area_accessible": "Area",
    "results_ar": "ASPECT RATIO",
    "results_ar_accessible": "Aspect Ratio",
    "results_mac": "M.A.C.",
    "results_mac_pos": "MAC POSITION",
    "results_mac_pos_accessible": "M.A.C. position — X from the root leading edge, Y from the symmetry axis",
    "results_cg25": "CG 25%",
    "results_cg25_accessible": "CG at 25% MAC, distance from the leading edge at the MAC station",
    "results_cg28": "CG 28%",
    "results_cg28_accessible": "CG at 28% MAC, distance from the leading edge at the MAC station",
    "results_cg30": "CG 30%",
    "results_cg30_accessible": "CG at 30% MAC, distance from the leading edge at the MAC station",
    "results_cg_custom": "CG (CUSTOM %)",
    "results_cg_custom_accessible": "CG at a custom (freely set) percent MAC",

    "preview_title": "Preview (top-down view)",
    "preview_accessible": "Wing preview (top-down view)",
    "preview_no_data": "No panel data",

    "stations_title": "Stations",
    "stations_header_station": "Station",
    "stations_header_y": "Y",
    "stations_header_le": "LE",
    "stations_header_te": "TE",
    "stations_header_chord": "Chord",
    "stations_accessible": "Wing station table",
    "station_root": "Root",
    "station_tip": "Tip",
    "station_mid": "S{n}",
    "station_mid_end": "S{n} (end of P{n})",
    "station_mid_start": "S{n} (start of P{p})",

    "default_project_name": "wing",
    "stations_filename_suffix": "_stations",

    "dialog_save_csv_title": "Save data (CSV)",
    "dialog_load_csv_title": "Load data (CSV)",
    "dialog_export_pdf_title": "Export PDF (model)",
    "dialog_export_stations_title": "Export stations (CSV)",
    "filter_csv": "CSV (*.csv)",
    "filter_pdf": "PDF (*.pdf)",

    "error_save_title": "Save error",
    "error_load_title": "Load error",
    "error_export_title": "Export error",
    "no_geometry_title": "No geometry",
    "no_geometry_body": "Enable at least one panel before exporting stations.",

    "status_saved": "Saved: {path}",
    "status_loaded": "Loaded: {path}",
    "status_exported_pdf": "Exported: {path}",
    "status_exported_stations": "Stations exported: {path}",

    "station_view_title_suffix": " — stations",
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
        "This panel is disabled — no geometry.\n"
        "Check the checkbox to enable it."
    ),

    "pdf_title": "GhostMEAN — Wing Model",
    "pdf_span": "Wing Span",
    "pdf_area": "Area",
    "pdf_ar": "Aspect Ratio",
    "pdf_mac": "M.A.C.",
    "pdf_mac_x": "MAC — position X",
    "pdf_mac_y": "MAC — position Y",
    "pdf_cg25": "CG 25% MAC (from LE at the MAC station)",
    "pdf_cg28": "CG 28% MAC (from LE at the MAC station)",
    "pdf_cg30": "CG 30% MAC (from LE at the MAC station)",
    "pdf_cg_custom": "CG {pct:.0f}% MAC (custom)",
    "menu_about": "About",
    "about_window_title": "About — GhostMEAN",
    "about_version_accessible": "Current application version",
    "about_link_wiki_accessible": "Open the project Wiki in your browser",
    "about_link_github_accessible": "Open the GitHub repository in your browser",
    "about_link_support_accessible": "Open the project Discussions on GitHub in your browser",
    "about_close": "Close",
}
