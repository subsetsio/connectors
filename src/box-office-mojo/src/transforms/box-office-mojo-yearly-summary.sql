SELECT
    CAST(year AS INTEGER)        AS year,
    TRY_CAST(regexp_replace(total_gross, '[^0-9]', '', 'g') AS BIGINT)      AS total_gross,
    TRY_CAST(regexp_replace(change_pct, '[^0-9.-]', '', 'g') AS DOUBLE)         AS change_vs_prior_year_pct,
    TRY_CAST(regexp_replace(releases, '[^0-9]', '', 'g') AS INTEGER)           AS releases,
    TRY_CAST(regexp_replace(average, '[^0-9]', '', 'g') AS BIGINT)          AS average_gross,
    num1_release                 AS num1_release
FROM "box-office-mojo-yearly-summary"
WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
