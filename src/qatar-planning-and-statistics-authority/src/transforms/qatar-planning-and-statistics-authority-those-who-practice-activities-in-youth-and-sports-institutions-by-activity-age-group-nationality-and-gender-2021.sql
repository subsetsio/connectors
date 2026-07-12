-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "activity",
    "activity_ar",
    "less_than_15_years_qataris_males",
    "less_than_15_years_qataris_females",
    "less_than_15_years_non_qataris_males",
    "less_than_15_years_non_qataris_females",
    "15_19_qataris_males",
    "15_19_qataris_females",
    "15_19_non_qataris_males",
    "15_19_non_qataris_females",
    "20_24_qataris_males",
    "20_24_qataris_females",
    "20_24_non_qataris_males",
    "20_24_non_qataris_females",
    "greater_than_25_years_qataris_males",
    "greater_than_25_years_qataris_females",
    "greater_than_25_years_non_qataris_males",
    "greater_than_25_years_non_qataris_females"
FROM "qatar-planning-and-statistics-authority-those-who-practice-activities-in-youth-and-sports-institutions-by-activity-age-group-nationality-and-gender-2021"
