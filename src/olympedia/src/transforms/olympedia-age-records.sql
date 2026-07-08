SELECT
    athlete,
    born,
    noc_code,
    discipline_sport,
    event,
    dates,
    placement,
    age
FROM "olympedia-age-records"
WHERE athlete IS NOT NULL
