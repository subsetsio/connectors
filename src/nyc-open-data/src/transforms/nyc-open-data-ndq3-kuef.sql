-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "date",
    "license_type",
    "license_no",
    "_name" AS name,
    "company",
    "disposition"
FROM "nyc-open-data-ndq3-kuef"
