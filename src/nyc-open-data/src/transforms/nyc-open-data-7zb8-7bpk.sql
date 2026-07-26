-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "class_1",
    "class_2",
    "class_3",
    "class_4"
FROM "nyc-open-data-7zb8-7bpk"
