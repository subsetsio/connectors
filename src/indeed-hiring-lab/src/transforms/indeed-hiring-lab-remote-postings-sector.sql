SELECT
    TRY_CAST("date" AS DATE)                      AS date,
    "jobcountry"                                  AS jobcountry,
    "normtitlecategory_consistent"               AS sector,
    TRY_CAST("remote_share_postings" AS DOUBLE)   AS remote_share_postings
FROM "indeed-hiring-lab-remote-postings-sector"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
