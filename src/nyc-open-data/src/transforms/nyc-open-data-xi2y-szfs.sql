-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geographic_unit",
    "student_category_1",
    "student_category_2",
    "number_of_students"
FROM "nyc-open-data-xi2y-szfs"
