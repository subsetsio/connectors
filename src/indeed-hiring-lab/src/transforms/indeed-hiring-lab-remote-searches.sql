SELECT
    TRY_CAST("date" AS DATE)                      AS date,
    "jobcountry"                                  AS jobcountry,
    TRY_CAST("remote_share_searches" AS DOUBLE)   AS remote_share_searches
FROM "indeed-hiring-lab-remote-searches"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
