SELECT
    state,
    CAST(year AS INTEGER)               AS year,
    metric,
    CAST(NULLIF(value, '') AS DOUBLE)   AS value
FROM "fhfa-enterprise-housing-goals"
