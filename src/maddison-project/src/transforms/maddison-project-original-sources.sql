SELECT
    countrycode,
    country,
    period,
    source,
    CAST(source_order AS INTEGER) AS source_order
FROM "maddison-project-original-sources"
WHERE source IS NOT NULL
