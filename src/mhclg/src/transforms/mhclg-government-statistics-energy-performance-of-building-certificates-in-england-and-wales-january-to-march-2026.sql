SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-energy-performance-of-building-certificates-in-england-and-wales-january-to-march-2026"
WHERE n_cols > 0
