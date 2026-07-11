-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study ethnicity and race" AS field_of_study_ethnicity_and_race,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Tenured - Number" AS tenured_number,
    "Tenured - SE" AS tenured_se,
    "Not tenured - On tenure track - Number" AS not_tenured_on_tenure_track_number,
    "Not tenured - On tenure track - SE" AS not_tenured_on_tenure_track_se,
    "Not tenured - Not on tenure track - Number" AS not_tenured_not_on_tenure_track_number,
    "Not tenured - Not on tenure track - SE" AS not_tenured_not_on_tenure_track_se,
    "Tenure not applicable - Not on tenure track - Number" AS tenure_not_applicable_not_on_tenure_track_number,
    "Tenure not applicable - Not on tenure track - SE" AS tenure_not_applicable_not_on_tenure_track_se
FROM "ncses-nsf25321-tab022"
