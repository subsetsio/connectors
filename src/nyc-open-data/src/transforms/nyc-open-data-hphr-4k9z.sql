-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_dbn",
    "of_students_over_five_active_on_register",
    "of_students_w_at_least_one_dose",
    "w_at_least_one_dose",
    "of_students_fully_vaccinated",
    "fully_vaccinated"
FROM "nyc-open-data-hphr-4k9z"
