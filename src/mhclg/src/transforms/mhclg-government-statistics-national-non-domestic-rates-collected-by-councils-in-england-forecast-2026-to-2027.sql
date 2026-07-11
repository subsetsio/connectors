SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-national-non-domestic-rates-collected-by-councils-in-england-forecast-2026-to-2027"
WHERE n_cols > 0
