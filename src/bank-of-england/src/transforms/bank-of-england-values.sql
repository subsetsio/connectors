SELECT
    series_code,
    obs_date,
    value
FROM (
    SELECT
        CAST(series_code AS VARCHAR) AS series_code,
        obs_date,
        TRY_CAST(value AS DOUBLE) AS value,
        row_number() OVER (
            PARTITION BY series_code, obs_date
            -- Defensive: the fetch requests each code exactly once, so a repeat
            -- of (code, date) would mean the source served it twice. Order by
            -- the parsed number, not the raw text, so the survivor is stable.
            ORDER BY TRY_CAST(value AS DOUBLE) DESC NULLS LAST
        ) AS _rn
    FROM "bank-of-england-values"
    WHERE series_code IS NOT NULL
      AND obs_date IS NOT NULL
)
WHERE _rn = 1
  AND value IS NOT NULL
