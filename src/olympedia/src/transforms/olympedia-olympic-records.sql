SELECT
    discipline_code,
    discipline,
    event,
    current_record,
    athletes,
    noc_code,
    games,
    date,
    phase,
    rank
FROM "olympedia-olympic-records"
WHERE event IS NOT NULL
