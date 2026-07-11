SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-number-of-fires-in-england-with-solar-panel-or-photovoltaic-panel-mentioned-in-the-additional-information-free-text"
WHERE n_cols > 0
