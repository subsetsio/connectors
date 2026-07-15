-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "flat_type",
    "child_dependency_ratio"
FROM "sg-data-d-8e83c90e9c5418c4e2f1475c6e8665e2"
