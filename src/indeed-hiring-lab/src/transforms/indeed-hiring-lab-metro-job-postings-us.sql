SELECT
    TRY_CAST("date" AS DATE)               AS date,
    "metro"                                AS metro,
    TRY_CAST("cbsa_code" AS INTEGER)       AS cbsa_code,
    TRY_CAST("indeed_job_postings_index" AS DOUBLE)     AS index
FROM "indeed-hiring-lab-metro-job-postings-us"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
