-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("measure56" AS BIGINT) AS measure56,
    "dimension1",
    "dimension2",
    "dimension3"
FROM "rosstat-7708234640-4livelihood"
