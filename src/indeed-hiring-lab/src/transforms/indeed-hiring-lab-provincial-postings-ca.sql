SELECT
    TRY_CAST("date" AS DATE)               AS date,
    "province"                              AS province,
    TRY_CAST("indeed_job_postings_index" AS DOUBLE)     AS index
FROM "indeed-hiring-lab-provincial-postings-ca"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
