SELECT
    TRY_CAST("date" AS DATE)                       AS date,
    "jobcountry"                                   AS jobcountry,
    TRY_CAST("indeed_job_postings_index" AS DOUBLE)             AS index,
    "variable"                                     AS variable,
    "display_name"                                 AS sector
FROM "indeed-hiring-lab-job-postings-by-sector"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
