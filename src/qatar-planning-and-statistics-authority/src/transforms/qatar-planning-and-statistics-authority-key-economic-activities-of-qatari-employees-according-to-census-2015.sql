-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity",
    "lnsht_lqtsdy",
    "code",
    "females_nth",
    "males_dhkwr",
    "percentage_to_the_total_qataris_in_all_economic_activities"
FROM "qatar-planning-and-statistics-authority-key-economic-activities-of-qatari-employees-according-to-census-2015"
