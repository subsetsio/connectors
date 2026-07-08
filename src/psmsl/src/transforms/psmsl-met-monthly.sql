SELECT
    station_id,
    make_date(year, month, 1) AS date,
    year,
    month,
    decimal_year,
    msl_mm,
    missing_flag,
    data_flag
FROM "psmsl-met-monthly"
WHERE msl_mm IS NOT NULL
