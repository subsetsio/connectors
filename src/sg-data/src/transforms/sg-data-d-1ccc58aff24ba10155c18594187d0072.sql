-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "releases_by_gender",
    "number_of_releases"
FROM "sg-data-d-1ccc58aff24ba10155c18594187d0072"
