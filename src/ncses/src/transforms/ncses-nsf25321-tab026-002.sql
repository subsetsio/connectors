-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Primary work activity" AS primary_work_activity,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "4-year educational institutiona - Number" AS 4_year_educational_institutiona_number,
    "4-year educational institutiona - SE" AS 4_year_educational_institutiona_se,
    "Other educational institutionb - Number" AS other_educational_institutionb_number,
    "Other educational institutionb - SE" AS other_educational_institutionb_se,
    "Private for profitc - Number" AS private_for_profitc_number,
    "Private for profitc - SE" AS private_for_profitc_se,
    "Private nonprofit - Number" AS private_nonprofit_number,
    "Private nonprofit - SE" AS private_nonprofit_se,
    "Federal government - Number" AS federal_government_number,
    "Federal government - SE" AS federal_government_se,
    "State or local government - Number" AS state_or_local_government_number,
    "State or local government - SE" AS state_or_local_government_se,
    "Self-employedd - Number" AS self_employedd_number,
    "Self-employedd - SE" AS self_employedd_se,
    "Othere - Number" AS othere_number,
    "Othere - SE" AS othere_se
FROM "ncses-nsf25321-tab026-002"
