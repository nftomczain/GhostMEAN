STRINGS = {
    "window_title": "GhostMEAN — Mean Aerodynamic Chord Calculator",

    "menu_file": "Файл",
    "menu_new_project": "Новый проект...",
    "menu_load_csv": "Загрузить данные (CSV)...",
    "menu_save_csv": "Сохранить данные (CSV)...",
    "menu_export_pdf": "Экспортировать PDF (модель)...",
    "menu_export_stations": "Экспортировать станции (CSV)...",
    "menu_export_stations_tooltip": (
        "Отдельный формат: полная, готовая геометрия (Y/LE/TE/хорда) на каждой станции — "
        "не для повторной загрузки, только для использования при постройке"
    ),

    "new_project_title": "Новый проект",
    "new_project_body": (
        "Очистить геометрию?\n"
        "Все панели будут сброшены к начальным значениям."
    ),
    "new_project_status": "Новый проект — геометрия сброшена",

    "topbar_units": "Единицы:",
    "topbar_units_accessible": "Выбор единиц измерения",
    "topbar_cg_custom": "CG — свой %:",
    "topbar_cg_custom_accessible": "Свой целевой процент MAC для CG",
    "topbar_show_dims": "Размеры на предпросмотре",
    "topbar_show_dims_accessible": "Показать размеры панелей на предпросмотре",
    "topbar_language": "Язык:",
    "topbar_language_accessible": "Выбор языка интерфейса",

    "panels_box_title": "Панели крыла (до 5)",
    "panel_label": "Панель {n}",
    "panel_enable_accessible": "Включить панель {n}",
    "panel_major_label": "Major:",
    "panel_minor_label": "Minor:",
    "panel_length_label": "Длина:",
    "panel_sweep_label": "Стреловидность (LE):",
    "panel_major_name": "Корневая хорда",
    "panel_minor_name": "Концевая хорда",
    "panel_length_name": "Длина панели",
    "panel_sweep_name": "Стреловидность передней кромки (LE) относительно оси размаха",
    "panel_disabled_hint": "\n\nОтметьте флажок «Панель N», чтобы редактировать эту панель",
    "panel_copy_tooltip": "Копировать панель {a} → панель {b}",
    "panel_copy_accessible": "Копировать панель {a} в панель {b}",
    "panel_copy_no_next_tooltip": "Нет следующей панели для копирования",
    "panel_stations_tooltip": "Показать точную геометрию (станции) панели {n}",
    "panel_stations_accessible": "Показать станции панели {n}",
    "panel_copied_status": "Панель {a} → Панель {b}: скопировано",

    "sweep_tooltip": (
        "Стреловидность ПЕРЕДНЕЙ КРОМКИ (Leading Edge) этой панели.\n"
        "Измеряется относительно оси размаха (перпендикулярной оси симметрии),\n"
        "НЕЗАВИСИМО для каждой панели — НЕ относительно предыдущей панели.\n"
        "Хорда не поворачивается вместе со стреловидностью — остаётся параллельной\n"
        "корневой хорде; стреловидность смещает в сторону только переднюю кромку."
    ),

    "warn_major_le_zero": "Панель {n}: Major ≤ 0",
    "warn_minor_le_zero": "Панель {n}: Minor ≤ 0",
    "warn_length_le_zero": "Панель {n}: Длина ≤ 0",
    "warn_minor_gt_major": "Панель {n}: Minor > Major (нетипичное сужение)",
    "warn_large_sweep": "Панель {n}: большая стреловидность ({v:.0f}°) — проверьте геометрию",
    "warn_discontinuity": (
        "Панель {b}: Major ({bm:.1f}мм) ≠ Minor панели {a} ({am:.1f}мм) — "
        "реальный скачок {jump:+.1f}мм виден на рисунке и в MAC"
    ),

    "results_title": "Результаты",
    "results_span": "РАЗМАХ КРЫЛА (WING SPAN)",
    "results_span_accessible": "Размах крыла (Wing Span)",
    "results_area": "ПЛОЩАДЬ (AREA)",
    "results_area_accessible": "Площадь (Area)",
    "results_ar": "УДЛИНЕНИЕ (ASPECT RATIO)",
    "results_ar_accessible": "Удлинение (Aspect Ratio)",
    "results_mac": "M.A.C.",
    "results_mac_pos": "ПОЛОЖЕНИЕ С.А.Х.",
    "results_mac_pos_accessible": "Положение С.А.Х. — X от передней кромки корня, Y от оси симметрии",
    "results_cg25": "CG 25%",
    "results_cg25_accessible": "CG при 25% MAC, расстояние от передней кромки на станции MAC",
    "results_cg28": "CG 28%",
    "results_cg28_accessible": "CG при 28% MAC, расстояние от передней кромки на станции MAC",
    "results_cg30": "CG 30%",
    "results_cg30_accessible": "CG при 30% MAC, расстояние от передней кромки на станции MAC",
    "results_cg_custom": "CG (СВОЙ %)",
    "results_cg_custom_accessible": "CG при своём (произвольно заданном) проценте MAC",

    "preview_title": "Предпросмотр (вид сверху)",
    "preview_accessible": "Предпросмотр крыла (вид сверху)",
    "preview_no_data": "Нет данных панели",

    "stations_title": "Станции",
    "stations_header_station": "Станция",
    "stations_header_y": "Y",
    "stations_header_le": "LE",
    "stations_header_te": "TE",
    "stations_header_chord": "Хорда",
    "stations_accessible": "Таблица станций крыла",
    "station_root": "Корень крыла",
    "station_tip": "Законцовка",
    "station_mid": "S{n}",
    "station_mid_end": "S{n} (конец P{n})",
    "station_mid_start": "S{n} (начало P{p})",

    "default_project_name": "krylo",
    "stations_filename_suffix": "_stancii",

    "dialog_save_csv_title": "Сохранить данные (CSV)",
    "dialog_load_csv_title": "Загрузить данные (CSV)",
    "dialog_export_pdf_title": "Экспортировать PDF (модель)",
    "dialog_export_stations_title": "Экспортировать станции (CSV)",
    "filter_csv": "CSV (*.csv)",
    "filter_pdf": "PDF (*.pdf)",

    "error_save_title": "Ошибка сохранения",
    "error_load_title": "Ошибка загрузки",
    "error_export_title": "Ошибка экспорта",
    "no_geometry_title": "Нет геометрии",
    "no_geometry_body": "Включите хотя бы одну панель перед экспортом станций.",

    "status_saved": "Сохранено: {path}",
    "status_loaded": "Загружено: {path}",
    "status_exported_pdf": "Экспортировано: {path}",
    "status_exported_stations": "Станции экспортированы: {path}",

    "station_view_title_suffix": " — станции",
    "station_view_panel_title": "ПАНЕЛЬ {n}",
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
        "Эта панель отключена — нет геометрии.\n"
        "Отметьте флажок, чтобы включить её."
    ),

    "pdf_title": "GhostMEAN — Модель крыла",
    "pdf_span": "Размах крыла (Wing Span)",
    "pdf_area": "Площадь (Area)",
    "pdf_ar": "Удлинение (Aspect Ratio)",
    "pdf_mac": "M.A.C.",
    "pdf_mac_x": "MAC — позиция X",
    "pdf_mac_y": "MAC — позиция Y",
    "pdf_cg25": "CG 25% MAC (от LE на станции MAC)",
    "pdf_cg28": "CG 28% MAC (от LE на станции MAC)",
    "pdf_cg30": "CG 30% MAC (от LE на станции MAC)",
    "pdf_cg_custom": "CG {pct:.0f}% MAC (свой)",
}
