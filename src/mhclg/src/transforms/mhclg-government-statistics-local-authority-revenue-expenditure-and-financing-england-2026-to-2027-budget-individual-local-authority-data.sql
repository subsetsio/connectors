SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-local-authority-revenue-expenditure-and-financing-england-2026-to-2027-budget-individual-local-authority-data"
WHERE n_cols > 0
