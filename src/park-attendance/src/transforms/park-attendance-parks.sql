SELECT
    CAST(park_id AS BIGINT)   AS park_id,
    park_name,
    company,
    country,
    continent,
    CAST(latitude AS DOUBLE)  AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    timezone
FROM "park-attendance-parks"
WHERE park_id IS NOT NULL
