-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Notes_on_merging_household_data:" AS notes_on_merging_household_data,
    "source_resource"
FROM "idb-baseline-salud-mesoamerica-panama-household-survey-2015"
