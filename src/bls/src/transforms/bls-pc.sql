SELECT
    series_id,
    year,
    period,
    CASE
        WHEN period BETWEEN 'M01' AND 'M12'
            THEN make_date(year, CAST(substr(period, 2, 2) AS INTEGER), 1)
        WHEN period IN ('Q01', 'Q02', 'Q03', 'Q04')
            THEN make_date(year, (CAST(substr(period, 2, 2) AS INTEGER) - 1) * 3 + 1, 1)
        WHEN period = 'S01' THEN make_date(year, 1, 1)
        WHEN period = 'S02' THEN make_date(year, 7, 1)
        ELSE make_date(year, 1, 1)
    END AS date,
    TRY_CAST(value AS DOUBLE) AS value,
    footnote_codes
FROM "bls-pc"
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY series_id, year, period ORDER BY footnote_codes) = 1
