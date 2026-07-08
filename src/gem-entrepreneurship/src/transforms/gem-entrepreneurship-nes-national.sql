SELECT
    CAST(year AS INTEGER)      AS year,
    economy_code,
    economy_name,
    economy_iso,
    indicator,
    variable,
    label,
    CAST(value AS DOUBLE)      AS value
FROM "gem-entrepreneurship-nes-national"
WHERE value IS NOT NULL
  AND indicator IS NOT NULL
