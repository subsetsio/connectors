-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "work_week_pattern",
    "distribution"
FROM "sg-data-d-4ed36511f052d872df7107d07d793da7"
