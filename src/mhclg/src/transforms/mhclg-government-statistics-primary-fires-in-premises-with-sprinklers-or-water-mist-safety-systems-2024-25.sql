SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-primary-fires-in-premises-with-sprinklers-or-water-mist-safety-systems-2024-25"
WHERE n_cols > 0
