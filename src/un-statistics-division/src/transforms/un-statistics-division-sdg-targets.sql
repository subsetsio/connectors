-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("goal" AS BIGINT) AS goal,
    "code",
    "title",
    "description",
    "uri",
    "indicators"
FROM "un-statistics-division-sdg-targets"
