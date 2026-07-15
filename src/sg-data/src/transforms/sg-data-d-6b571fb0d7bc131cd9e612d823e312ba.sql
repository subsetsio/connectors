-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "academic_programme",
    "results",
    "percentage_of_inmates"
FROM "sg-data-d-6b571fb0d7bc131cd9e612d823e312ba"
