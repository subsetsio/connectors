SELECT
    TRY_CAST("date" AS DATE)               AS date,
    "region"                              AS region,
    TRY_CAST("indeed_job_postings_index" AS DOUBLE)     AS index
FROM "indeed-hiring-lab-regional-gb"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
