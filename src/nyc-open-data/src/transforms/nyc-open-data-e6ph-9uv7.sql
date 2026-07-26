-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_name" AS name,
    "subject",
    "status",
    "link"
FROM "nyc-open-data-e6ph-9uv7"
