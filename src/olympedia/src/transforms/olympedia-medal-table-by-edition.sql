SELECT
    CAST(edition_id AS INTEGER) AS edition_id,
    TRY_CAST(year AS INTEGER)   AS year,
    season,
    category,
    noc_code,
    country,
    CAST(gold AS INTEGER)   AS gold,
    CAST(silver AS INTEGER) AS silver,
    CAST(bronze AS INTEGER) AS bronze,
    CAST(total AS INTEGER)  AS total
FROM "olympedia-medal-table-by-edition"
WHERE edition_id IS NOT NULL AND noc_code IS NOT NULL
