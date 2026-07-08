WITH base AS (
    SELECT *, CAST(period AS VARCHAR) AS p
    FROM "oenb-100140001"
)
SELECT
    CASE freq
        WHEN 'A' THEN make_date(TRY_CAST(p AS INTEGER), 1, 1)
        WHEN 'M' THEN make_date(
            TRY_CAST(substr(p, 1, 4) AS INTEGER),
            TRY_CAST(substr(p, 6, 2) AS INTEGER), 1)
        WHEN 'Q' THEN make_date(
            TRY_CAST(substr(p, 1, 4) AS INTEGER),
            (TRY_CAST(substr(p, 7, 1) AS INTEGER) - 1) * 3 + 1, 1)
        WHEN 'H' THEN make_date(  -- half-year periods are 'YYYY-B1' / 'YYYY-B2'
            TRY_CAST(substr(p, 1, 4) AS INTEGER),
            (TRY_CAST(substr(p, 7, 1) AS INTEGER) - 1) * 6 + 1, 1)
        WHEN 'D' THEN TRY_CAST(p AS DATE)
        ELSE NULL
    END                              AS date,
    p                                AS period,
    freq                             AS frequency,
    pos                              AS series_code,
    pos_title                        AS series_name,
    dim_key                          AS dimensions,
    TRY_CAST(value AS DOUBLE)        AS value,
    unit_text                        AS unit,
    TRY_CAST(unit_mult AS INTEGER)   AS unit_mult
FROM base
WHERE value IS NOT NULL
