SELECT
    TRY_CAST("date" AS DATE)               AS date,
    "Metro"                              AS metro,
    TRY_CAST("indeed_job_postings_index" AS DOUBLE)     AS index
FROM "indeed-hiring-lab-metro-job-postings-ca"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
