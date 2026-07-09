SELECT
    trim(year) AS year,
    TRY_CAST(split_part(trim(year), '-', 1) AS INTEGER) AS year_start,
    TRY_CAST(coal AS DOUBLE)          AS coal_mw,
    TRY_CAST(gas AS DOUBLE)           AS gas_mw,
    TRY_CAST(diesel AS DOUBLE)        AS diesel_mw,
    TRY_CAST(thermal_total AS DOUBLE) AS thermal_total_mw,
    TRY_CAST(nuclear AS DOUBLE)       AS nuclear_mw,
    TRY_CAST(hydro AS DOUBLE)         AS hydro_mw,
    TRY_CAST(res AS DOUBLE)           AS res_mw,
    TRY_CAST(gtotal AS DOUBLE)        AS total_mw
FROM "cea-india-installed-capacity-composition"
WHERE year IS NOT NULL AND trim(year) <> ''
