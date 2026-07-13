-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    "authors",
    "author_affiliation",
    "department",
    "author_country",
    "source_resource"
FROM "idb-building-stronger-transport-policy-an-evidence-gap-map-dataset"
