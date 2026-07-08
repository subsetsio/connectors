SELECT
    country_code,
    metric,
    CAST(field_id AS INTEGER) AS field_id,
    CAST(year AS INTEGER)     AS year,
    CAST(value AS BIGINT)     AS value
FROM "epo-patent-applications-grants"
WHERE value IS NOT NULL AND value <> ''
