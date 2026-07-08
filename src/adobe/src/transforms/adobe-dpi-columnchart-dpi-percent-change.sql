SELECT
    CAST(_file_date AS DATE) AS date,
    category,
    TRY_CAST(val AS DOUBLE) AS percent_change
FROM (
    UNPIVOT "adobe-dpi-columnchart-dpi-percent-change"
    ON COLUMNS(* EXCLUDE ("month", "_file_ym", "_file_date"))
    INTO NAME category VALUE val
)
WHERE TRY_CAST(val AS DOUBLE) IS NOT NULL
ORDER BY date, category
