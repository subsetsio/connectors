SELECT
    CAST(country_id AS BIGINT) AS country_id,
    iso,
    short_name,
    long_name,
    classifications
FROM "itu-countries"
WHERE iso IS NOT NULL
