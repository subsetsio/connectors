-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of study" AS field_of_study,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "4-year educational institutiona - Median salary" AS "4_year_educational_institutiona_median_salary",
    "4-year educational institutiona - SE" AS "4_year_educational_institutiona_se",
    "Other educational institutionb - Median salary" AS other_educational_institutionb_median_salary,
    "Other educational institutionb - SE" AS other_educational_institutionb_se,
    "Private for profitc - Median salary" AS private_for_profitc_median_salary,
    "Private for profitc - SE" AS private_for_profitc_se,
    "Private nonprofit - Median salary" AS private_nonprofit_median_salary,
    "Private nonprofit - SE" AS private_nonprofit_se,
    "Federal government - Median salary" AS federal_government_median_salary,
    "Federal government - SE" AS federal_government_se,
    "State or local government - Median salary" AS state_or_local_government_median_salary,
    "State or local government - SE" AS state_or_local_government_se,
    "Self-employedd - Median salary" AS self_employedd_median_salary,
    "Self-employedd - SE" AS self_employedd_se,
    "Othere - Median salary" AS othere_median_salary,
    "Othere - SE" AS othere_se
FROM "ncses-nsf25321-tab054"
