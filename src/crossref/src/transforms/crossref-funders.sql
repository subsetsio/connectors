-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("funder_id" AS BIGINT) AS funder_id,
    "name",
    "location",
    "uri"
FROM "crossref-funders"
