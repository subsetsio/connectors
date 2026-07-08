SELECT DISTINCT
    CAST(validFor AS DATE)    AS date,
    period                    AS term,
    CAST(pribor AS DOUBLE)    AS rate
FROM "czech-national-bank-pribor-daily"
WHERE validFor IS NOT NULL AND pribor IS NOT NULL
