-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation and age" AS occupation_and_age,
    "All degrees - Total" AS all_degrees_total,
    "All degrees - Female" AS all_degrees_female,
    "All degrees - Male" AS all_degrees_male,
    "Bachelor's - Total" AS bachelor_s_total,
    "Bachelor's - Female" AS bachelor_s_female,
    "Bachelor's - Male" AS bachelor_s_male,
    "Master's - Total" AS master_s_total,
    "Master's - Female" AS master_s_female,
    "Master's - Male" AS master_s_male,
    "Doctorate - Total" AS doctorate_total,
    "Doctorate - Female" AS doctorate_female,
    "Doctorate - Male" AS doctorate_male,
    "Professional - Total" AS professional_total,
    "Professional - Female" AS professional_female,
    "Professional - Male" AS professional_male
FROM "ncses-nsf25322-tab004-001"
