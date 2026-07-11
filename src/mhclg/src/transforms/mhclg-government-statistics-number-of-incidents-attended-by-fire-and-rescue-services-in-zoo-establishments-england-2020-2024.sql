SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-number-of-incidents-attended-by-fire-and-rescue-services-in-zoo-establishments-england-2020-2024"
WHERE n_cols > 0
