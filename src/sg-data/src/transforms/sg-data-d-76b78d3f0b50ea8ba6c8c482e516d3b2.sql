-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "releases_by_gender",
    "number_of_releases"
FROM "sg-data-d-76b78d3f0b50ea8ba6c8c482e516d3b2"
