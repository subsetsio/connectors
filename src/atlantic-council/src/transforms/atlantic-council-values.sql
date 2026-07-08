SELECT
    entity_id,
    entity_type,
    name,
    CAST(year AS INTEGER)  AS year,
    indicator_code,
    CAST(value AS DOUBLE)  AS value,
    CAST(rank AS INTEGER)  AS rank
FROM "atlantic-council-values"
WHERE value IS NOT NULL
