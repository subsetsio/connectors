-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "service_taxonomy_id",
    "service_id",
    "taxonomy_id"
FROM "nyc-open-data-bwhw-9jek"
