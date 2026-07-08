SELECT
    CAST(id AS BIGINT)            AS id,
    region,
    scenario,
    sector,
    indicator,
    variable,
    CAST(year AS INTEGER)         AS year,
    CAST(value AS DOUBLE)         AS value,
    unit,
    per_capita,
    version,
    comments,
    source,
    CAST(edition AS INTEGER)      AS edition
FROM "climate-action-tracker-country-emissions"
WHERE value IS NOT NULL
