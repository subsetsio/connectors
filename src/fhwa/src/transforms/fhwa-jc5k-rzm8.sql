SELECT
    state,
    api_url.url AS api_url,
    map_url.url AS map_url
FROM "fhwa-jc5k-rzm8"
WHERE state IS NOT NULL
