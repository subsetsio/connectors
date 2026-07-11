SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-fire-and-rescue-percentage-of-incidents-by-hour-of-the-day-england-2010-to-2025"
WHERE n_cols > 0
