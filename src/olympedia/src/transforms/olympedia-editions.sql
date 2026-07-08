SELECT
    CAST(edition_id AS INTEGER) AS edition_id,
    category,
    season,
    TRY_CAST(year AS INTEGER)   AS year,
    city,
    host_noc,
    opened,
    closed,
    competition
FROM "olympedia-editions"
WHERE edition_id IS NOT NULL
