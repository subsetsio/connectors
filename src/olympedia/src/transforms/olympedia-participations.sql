SELECT
    athlete,
    nations,
    sports,
    roles,
    era,
    TRY_CAST(participations AS INTEGER) AS participations
FROM "olympedia-participations"
WHERE athlete IS NOT NULL
