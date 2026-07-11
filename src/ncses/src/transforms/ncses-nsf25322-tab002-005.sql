-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation sex ethnicity race and disability status" AS occupation_sex_ethnicity_race_and_disability_status,
    "Total" AS total,
    "Business or industry - Business or industry total" AS business_or_industry_business_or_industry_total,
    "Business or industry - For-profit business or industry" AS business_or_industry_for_profit_business_or_industry,
    "Business or industry - Nonprofit business or industry" AS business_or_industry_nonprofit_business_or_industry,
    "Business or industry - Self-employed not incorporated" AS business_or_industry_self_employed_not_incorporated,
    "Education - Education total" AS education_education_total,
    "Education - 4-year educational institutiona" AS education_4_year_educational_institutiona,
    "Education - 2-year college or precollege educational institution" AS education_2_year_college_or_precollege_educational_institution,
    "Government - Government total" AS government_government_total,
    "Government - Federal governmentb" AS government_federal_governmentb,
    "Government - State or local government" AS government_state_or_local_government
FROM "ncses-nsf25322-tab002-005"
