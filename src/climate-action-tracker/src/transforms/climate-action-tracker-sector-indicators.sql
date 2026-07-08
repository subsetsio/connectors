SELECT
    CAST(id AS BIGINT)            AS id,
    country,
    scenario,
    sector,
    indicator,
    variable,
    CAST(year AS INTEGER)         AS year,
    CAST(value AS DOUBLE)         AS value,
    unit,
    CAST(normalized_value AS DOUBLE) AS normalized_value,
    CAST(edition AS INTEGER)      AS edition
FROM "climate-action-tracker-sector-indicators"
WHERE value IS NOT NULL
