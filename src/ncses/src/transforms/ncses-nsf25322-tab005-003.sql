-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of highest degree father's education and mother's education" AS field_of_highest_degree_father_s_education_and_mother_s_education,
    "Bachelor's - Total" AS bachelor_s_total,
    "Bachelor's - $0" AS bachelor_s_0,
    "Bachelor's - $1–$10 000" AS bachelor_s_1_10_000,
    "Bachelor's - $10 001–$20 000" AS bachelor_s_10_001_20_000,
    "Bachelor's - $20 001–$30 000" AS bachelor_s_20_001_30_000,
    "Bachelor's - $30 001 and over" AS bachelor_s_30_001_and_over,
    "Master's - Total" AS master_s_total,
    "Master's - $0" AS master_s_0,
    "Master's - $1–$10 000" AS master_s_1_10_000,
    "Master's - $10 001–$20 000" AS master_s_10_001_20_000,
    "Master's - $20 001–$30 000" AS master_s_20_001_30_000,
    "Master's - $30 001 and over" AS master_s_30_001_and_over,
    "Doctorate - Total" AS doctorate_total,
    "Doctorate - $0" AS doctorate_0,
    "Doctorate - $1–$10 000" AS doctorate_1_10_000,
    "Doctorate - $10 001–$20 000" AS doctorate_10_001_20_000,
    "Doctorate - $20 001–$30 000" AS doctorate_20_001_30_000,
    "Doctorate - $30 001 and over" AS doctorate_30_001_and_over,
    "Professional - Total" AS professional_total,
    "Professional - $0" AS professional_0,
    "Professional - $1–$10 000" AS professional_1_10_000,
    "Professional - $10 001–$20 000" AS professional_10_001_20_000,
    "Professional - $20 001–$30 000" AS professional_20_001_30_000,
    "Professional - $30 001 and over" AS professional_30_001_and_over
FROM "ncses-nsf25322-tab005-003"
