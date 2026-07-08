SELECT
    TRY_CAST("date" AS DATE)                          AS date,
    "jobcountry"                                      AS jobcountry,
    TRY_CAST("indeed_job_postings_index_SA" AS DOUBLE)  AS index_sa,
    TRY_CAST("indeed_job_postings_index_NSA" AS DOUBLE) AS index_nsa,
    "variable"                                        AS variable
FROM "indeed-hiring-lab-aggregate-job-postings"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
