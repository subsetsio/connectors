-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "grade",
    "_year" AS year,
    "number_tested",
    "level_3_or_higher",
    "level_3_or_higher_1"
FROM "nyc-open-data-xw3c-8982"
