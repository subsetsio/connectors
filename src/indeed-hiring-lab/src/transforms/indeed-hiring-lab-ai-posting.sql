SELECT
    TRY_CAST("date" AS DATE)                  AS date,
    "jobcountry"                              AS jobcountry,
    TRY_CAST("AI_share_postings" AS DOUBLE)   AS ai_share_postings
FROM "indeed-hiring-lab-ai-posting"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
