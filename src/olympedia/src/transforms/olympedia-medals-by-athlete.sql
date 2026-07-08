SELECT
    athlete,
    noc_code,
    CAST(gold AS INTEGER)   AS gold,
    CAST(silver AS INTEGER) AS silver,
    CAST(bronze AS INTEGER) AS bronze,
    CAST(total AS INTEGER)  AS total
FROM "olympedia-medals-by-athlete"
WHERE athlete IS NOT NULL
