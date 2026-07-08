SELECT
    station_id,
    year,
    make_date(year, 1, 1) AS date,
    msl_mm,
    missing_flag,
    data_flag
FROM "psmsl-rlr-annual"
WHERE msl_mm IS NOT NULL
