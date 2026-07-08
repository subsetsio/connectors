SELECT
    discipline_code,
    discipline,
    sport,
    season,
    CAST(olympic_status AS BOOLEAN) AS olympic_status
FROM "olympedia-sports"
WHERE discipline_code IS NOT NULL
