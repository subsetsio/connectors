-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field and primary source of support" AS field_and_primary_source_of_support,
    "Totala" AS totala,
    "Sex - Male" AS sex_male,
    "Sex - Female" AS sex_female,
    "Citizenship status - U.S. citizen or permanent resident" AS citizenship_status_u_s_citizen_or_permanent_resident,
    "Citizenship status - Temporary visa holder" AS citizenship_status_temporary_visa_holder,
    "U.S. citizens and permanent residents - Hispanic or Latino - Temporary visa holder" AS u_s_citizens_and_permanent_residents_hispanic_or_latino_temporary_visa_holder,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - American Indian or Alaska Native" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_american_indian_or_alaska_native,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Asian" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_asian,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Black or African American" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_black_or_african_american,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - White" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_white,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - More than one race" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_more_than_one_race,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Other race or race not reported" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_other_race_or_race_not_reported,
    "U.S. citizens and permanent residents - Ethnicity not reported - Other race or race not reported" AS u_s_citizens_and_permanent_residents_ethnicity_not_reported_other_race_or_race_not_reported
FROM "ncses-nsf25349-tab004-001"
