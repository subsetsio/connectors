-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_groups_in_years",
    "age_groups_in_years_ar",
    "nationality",
    "nationality_ar",
    "females_secondary",
    "males_university",
    "females_university",
    "higher_studies_males",
    "higher_studies_females",
    "males_less_than_secandary",
    "females_less_than_secandary",
    "males_secandary"
FROM "qatar-planning-and-statistics-authority-non-employee-trainees-at-private-training-centers-by-educational-status-gender-nationality-and-age-group"
