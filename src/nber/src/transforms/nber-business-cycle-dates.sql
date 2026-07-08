SELECT
    CAST(peak AS DATE)   AS peak_date,
    CAST(trough AS DATE) AS trough_date
FROM "nber-business-cycle-dates"
