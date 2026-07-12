-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "type_of_laboratory",
    "type_of_laboratory_ar",
    "number_of_laboratory_tests_dd_lthlyl_lmkhtbry"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-laboratory-tests-done-in-hamad-medical-corporation-by-type-of-laboratory"
