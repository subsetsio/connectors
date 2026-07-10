-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("goal" AS BIGINT) AS goal,
    "target",
    "code",
    "description",
    CAST("tier" AS BIGINT) AS tier,
    "uri",
    "series"
FROM "un-statistics-division-sdg-indicators"
