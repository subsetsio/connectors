SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-deliberate-primary-fires-fatalities-and-non-fatal-casualties-by-source-of-ignition-england-202425"
WHERE n_cols > 0
