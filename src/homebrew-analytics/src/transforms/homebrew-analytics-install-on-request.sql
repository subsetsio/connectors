SELECT
    "window"                   AS window,
    CAST(window_start AS DATE) AS window_start,
    CAST(window_end   AS DATE) AS window_end,
    CAST(rank AS INTEGER)      AS rank,
    item                       AS formula,
    CAST(count AS BIGINT)      AS count,
    CAST(percent AS DOUBLE)    AS percent
FROM "homebrew-analytics-install-on-request"
WHERE count > 0
