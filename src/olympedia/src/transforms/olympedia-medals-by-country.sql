SELECT
    noc_code,
    country,
    CAST(gold AS INTEGER)   AS gold,
    CAST(silver AS INTEGER) AS silver,
    CAST(bronze AS INTEGER) AS bronze,
    CAST(total AS INTEGER)  AS total
FROM "olympedia-medals-by-country"
WHERE noc_code IS NOT NULL
