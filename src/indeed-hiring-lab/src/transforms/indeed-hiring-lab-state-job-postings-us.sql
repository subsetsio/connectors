SELECT
    TRY_CAST("date" AS DATE)               AS date,
    "state"                              AS state,
    TRY_CAST("indeed_job_postings_index" AS DOUBLE)     AS index
FROM "indeed-hiring-lab-state-job-postings-us"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
