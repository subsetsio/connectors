SELECT
    TRY_CAST(strptime(
        regexp_extract(date_raw, '^[A-Za-z]{3} [0-9]{1,2}') || ' ' || year,
        '%b %d %Y') AS DATE)     AS date,
    CAST(year AS INTEGER)        AS year,
    day_of_week                  AS day_of_week,
    TRY_CAST(regexp_replace(day_num, '[^0-9]', '', 'g') AS INTEGER)            AS day_of_year,
    TRY_CAST(regexp_replace(top10_gross, '[^0-9]', '', 'g') AS BIGINT)      AS top10_gross,
    TRY_CAST(regexp_replace(change_yd_pct, '[^0-9.-]', '', 'g') AS DOUBLE)      AS change_vs_yesterday_pct,
    TRY_CAST(regexp_replace(change_lw_pct, '[^0-9.-]', '', 'g') AS DOUBLE)      AS change_vs_last_week_pct,
    TRY_CAST(regexp_replace(releases, '[^0-9]', '', 'g') AS INTEGER)           AS releases,
    num1_release                 AS num1_release,
    TRY_CAST(regexp_replace(gross, '[^0-9]', '', 'g') AS BIGINT)            AS num1_gross
FROM "box-office-mojo-domestic-daily"
WHERE TRY_CAST(strptime(
        regexp_extract(date_raw, '^[A-Za-z]{3} [0-9]{1,2}') || ' ' || year,
        '%b %d %Y') AS DATE) IS NOT NULL
