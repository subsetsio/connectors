SELECT
    CAST(year AS INTEGER)        AS year,
    TRY_CAST(regexp_replace(week, '[^0-9]', '', 'g') AS INTEGER)               AS week,
    (long_weekend = 'True')      AS long_weekend,
    dates                        AS dates,
    TRY_CAST(regexp_replace(top10_gross, '[^0-9]', '', 'g') AS BIGINT)      AS top10_gross,
    TRY_CAST(regexp_replace(top10_change_pct, '[^0-9.-]', '', 'g') AS DOUBLE)   AS top10_change_pct,
    TRY_CAST(regexp_replace(overall_gross, '[^0-9]', '', 'g') AS BIGINT)    AS overall_gross,
    TRY_CAST(regexp_replace(overall_change_pct, '[^0-9.-]', '', 'g') AS DOUBLE) AS overall_change_pct,
    TRY_CAST(regexp_replace(releases, '[^0-9]', '', 'g') AS INTEGER)           AS releases,
    num1_release                 AS num1_release
FROM "box-office-mojo-weekend-summary"
WHERE TRY_CAST(regexp_replace(week, '[^0-9]', '', 'g') AS INTEGER) IS NOT NULL
