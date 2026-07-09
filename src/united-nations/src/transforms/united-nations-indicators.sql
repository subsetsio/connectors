-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator_code",
    CAST("goal_code" AS BIGINT) AS goal_code,
    "target_code",
    "description",
    CAST("tier" AS BIGINT) AS tier,
    "uri",
    "series_count",
    "series_codes"
FROM "united-nations-indicators"
