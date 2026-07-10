-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe highlight categories rather than the full constituency universe; do not treat this as one row per parliamentary constituency.
SELECT
    "state_ut___code" AS state_ut_code,
    "constituency_name___code" AS constituency_name_code,
    CAST("const__no_" AS BIGINT) AS constituency_no,
    "candidates_" AS candidates_category,
    CAST(NULLIF("male", 'NA') AS BIGINT) AS male,
    CAST(NULLIF("female", 'NA') AS BIGINT) AS female,
    CAST(NULLIF("_tg_", 'NA') AS BIGINT) AS third_gender,
    CAST(NULLIF("_total", 'NA') AS BIGINT) AS total
FROM "election-commission-of-india-a27ba4e9-73c2-40d1-90b2-41d71ea7c283"
