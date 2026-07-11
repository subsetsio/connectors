SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-average-area-of-fire-damage-in-dwellings-and-other-buildings-2010-11-to-2023-24"
WHERE n_cols > 0
