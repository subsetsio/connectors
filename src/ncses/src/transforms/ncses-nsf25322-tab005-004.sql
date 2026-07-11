-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Place of birth level of highest degree and occupation" AS place_of_birth_level_of_highest_degree_and_occupation,
    "Total" AS total,
    "Business or industry" AS business_or_industry,
    "4-year educational institutiona" AS 4_year_educational_institutiona,
    "2-year college or precollege educational institution" AS 2_year_college_or_precollege_educational_institution,
    "Governmentb" AS governmentb
FROM "ncses-nsf25322-tab005-004"
