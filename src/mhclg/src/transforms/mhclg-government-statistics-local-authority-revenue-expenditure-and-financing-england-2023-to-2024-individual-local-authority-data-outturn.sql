SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-local-authority-revenue-expenditure-and-financing-england-2023-to-2024-individual-local-authority-data-outturn"
WHERE n_cols > 0
