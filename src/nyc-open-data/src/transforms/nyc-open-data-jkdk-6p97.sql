-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "req",
    "comp_date",
    "_location" AS location,
    "type_name",
    "_comments" AS comments,
    "_ref" AS ref
FROM "nyc-open-data-jkdk-6p97"
