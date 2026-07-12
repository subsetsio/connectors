SELECT
    CAST(year AS VARCHAR) AS year,
    CAST(country AS VARCHAR) AS country,
    CAST(payloads AS BIGINT) AS payloads,
    CAST(rocket_bodies AS BIGINT) AS rocket_bodies,
    CAST(debris AS BIGINT) AS debris,
    CAST(total AS BIGINT) AS total
FROM "celestrak-launches-by-country"
