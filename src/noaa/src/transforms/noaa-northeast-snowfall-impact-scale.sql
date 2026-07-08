SELECT
    TRY_CAST(regexp_replace("Rank", '[^0-9]', '', 'g') AS INT) AS rank,
    try_strptime("Start Date", '%m/%d/%Y')::DATE               AS start_date,
    try_strptime("End Dat", '%m/%d/%Y')::DATE                  AS end_date,
    TRY_CAST(NESIS AS DOUBLE)                                  AS nesis,
    TRY_CAST(Category AS INT)                                  AS category,
    Description                                                AS description
FROM "noaa-northeast-snowfall-impact-scale"
WHERE TRY_CAST(regexp_replace("Rank", '[^0-9]', '', 'g') AS INT) IS NOT NULL
