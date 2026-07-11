SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-primary-fires-fatalities-and-casualties-in-care-homes-in-england-by-source-of-ignition-and-victim-age-and-gender"
WHERE n_cols > 0
