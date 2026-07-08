SELECT
    geo,
    year                          AS year_range,
    indicator,
    series,
    taxonomic_group,
    unit_measure                  AS unit,
    value                         AS value_raw,
    TRY_CAST(REPLACE(value, ',', '') AS DOUBLE) AS value,
    obs_status,
    note,
    source
FROM "unodc-data-wildlife-trafficking"
WHERE value IS NOT NULL
