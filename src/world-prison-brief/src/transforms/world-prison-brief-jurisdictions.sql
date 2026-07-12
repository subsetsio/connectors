-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "jurisdiction_id",
    "name",
    "region",
    "country_path",
    "country_url"
FROM "world-prison-brief-jurisdictions"
