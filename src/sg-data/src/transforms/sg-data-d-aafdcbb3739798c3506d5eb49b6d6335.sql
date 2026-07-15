-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rank",
    "latest_year",
    "report",
    "country"
FROM "sg-data-d-aafdcbb3739798c3506d5eb49b6d6335"
