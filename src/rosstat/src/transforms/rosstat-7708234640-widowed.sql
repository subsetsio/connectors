-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("measure14" AS BIGINT) AS measure14,
    CAST("dimension1" AS BIGINT) AS dimension1,
    "dimension2",
    "dimension3"
FROM "rosstat-7708234640-widowed"
