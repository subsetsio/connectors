SELECT
    TRY_CAST("date" AS DATE)               AS date,
    "cities"                              AS city,
    TRY_CAST("indeed_job_postings_index" AS DOUBLE)     AS index
FROM "indeed-hiring-lab-city-postings-gb"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
