SELECT
    CAST(state_ut___code AS VARCHAR)          AS state_ut_code,
    CAST(constituency_name___code AS VARCHAR) AS constituency_name_code,
    TRY_CAST(const__no_ AS BIGINT)            AS constituency_no,
    CAST(candidates_ AS VARCHAR)              AS candidates_category,
    TRY_CAST(male AS BIGINT)                  AS male,
    TRY_CAST(female AS BIGINT)                AS female,
    TRY_CAST("_tg_" AS BIGINT)                AS third_gender,
    TRY_CAST("_total" AS BIGINT)              AS total
FROM "election-commission-of-india-a27ba4e9-73c2-40d1-90b2-41d71ea7c283"
WHERE constituency_name___code IS NOT NULL
