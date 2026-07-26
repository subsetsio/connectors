-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "total_students",
    "students_in_temporary_housing",
    "students_in_temporary_housing_1",
    "students_residing_in_shelter",
    "residing_in_dhs_shelter",
    "residing_in_nondhs_shelter",
    "doubled_up"
FROM "nyc-open-data-3wtp-43m9"
