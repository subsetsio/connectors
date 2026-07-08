SELECT * REPLACE (
    TRY_CAST(entry_date AS DATE)  AS entry_date,
    TRY_CAST(last_update AS DATE) AS last_update
)
FROM "em-dat-events"
WHERE dis_no IS NOT NULL
