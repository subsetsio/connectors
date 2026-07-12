-- caution: This catalog mixes many BOJ database groups and frequencies; filter by db, category, layer fields, or series_code before interpreting series together.
SELECT
    db,
    series_code,
    name,
    unit,
    frequency,
    category,
    layer1, layer2, layer3, layer4, layer5,
    -- Catalog dates arrive at mixed widths by frequency: YYYYMMDD
    -- (daily), YYYYMM (monthly/quarterly), YYYY (annual). strptime
    -- *raises* on a width mismatch and TRY_CAST does not catch a
    -- function error, so parse with try_strptime (NULL on miss) and
    -- coalesce widest-first, defaulting the missing parts to the 1st.
    COALESCE(
        try_strptime(NULLIF(start_date, ''), '%Y%m%d'),
        try_strptime(NULLIF(start_date, ''), '%Y%m'),
        try_strptime(NULLIF(start_date, ''), '%Y')
    )::DATE AS start_date,
    COALESCE(
        try_strptime(NULLIF(end_date, ''), '%Y%m%d'),
        try_strptime(NULLIF(end_date, ''), '%Y%m'),
        try_strptime(NULLIF(end_date, ''), '%Y')
    )::DATE AS end_date,
    COALESCE(
        try_strptime(NULLIF(last_update, ''), '%Y%m%d'),
        try_strptime(NULLIF(last_update, ''), '%Y%m'),
        try_strptime(NULLIF(last_update, ''), '%Y')
    )::DATE AS last_update,
    notes
FROM "bank-of-japan-series"
WHERE series_code IS NOT NULL AND series_code <> ''
QUALIFY row_number() OVER (
    PARTITION BY db, series_code
    ORDER BY last_update DESC NULLS LAST
) = 1
