SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-local-authority-capital-expenditure-and-receipts-in-england-2024-to-2025-provisional-outturn-and-2025-to-2026-forecast"
WHERE n_cols > 0
