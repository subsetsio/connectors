-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "admissions_by_main_offence_group",
    "number_of_admissions"
FROM "sg-data-d-e618ac4c45fce4110df180ba905215f7"
