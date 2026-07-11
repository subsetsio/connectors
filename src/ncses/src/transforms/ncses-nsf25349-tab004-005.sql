-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Debt level - Cumulative debt" AS debt_level_cumulative_debt,
    "Sex - Male - Cumulative debt" AS sex_male_cumulative_debt,
    "Sex - Male - Cumulative debt_2" AS sex_male_cumulative_debt_2,
    "Sex - Female - Cumulative debt" AS sex_female_cumulative_debt,
    "Sex - Female - Cumulative debt_2" AS sex_female_cumulative_debt_2,
    "Citizenship status - U.S. citizen or permanent resident - Cumulative debt" AS citizenship_status_u_s_citizen_or_permanent_resident_cumulative_debt,
    "Citizenship status - U.S. citizen or permanent resident - Cumulative debt_2" AS citizenship_status_u_s_citizen_or_permanent_resident_cumulative_debt_2,
    "Citizenship status - Temporary visa holder - Cumulative debt" AS citizenship_status_temporary_visa_holder_cumulative_debt,
    "Citizenship status - Temporary visa holder - Cumulative debt_2" AS citizenship_status_temporary_visa_holder_cumulative_debt_2,
    "U.S. citizens and permanent residents - Hispanic or Latino - Temporary visa holder - Cumulative debt" AS u_s_citizens_and_permanent_residents_hispanic_or_latino_temporary_visa_holder_cumulative_debt,
    "U.S. citizens and permanent residents - Hispanic or Latino - Temporary visa holder - Cumulative debt_2" AS u_s_citizens_and_permanent_residents_hispanic_or_latino_temporary_visa_holder_cumulative_debt_2,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - American Indian or Alaska Native - Cumulative debt" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_american_indian_or_alaska_native_cumulative_debt,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - American Indian or Alaska Native - Cumulative debt_2" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_american_indian_or_alaska_native_cumulative_debt_2,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Asian - Cumulative debt" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_asian_cumulative_debt,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Asian - Cumulative debt_2" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_asian_cumulative_debt_2,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Black or African American - Cumulative debt" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_black_or_african_american_cumulative_debt,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Black or African American - Cumulative debt_2" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_black_or_african_american_cumulative_debt_2,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - White - Cumulative debt" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_white_cumulative_debt,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - White - Cumulative debt_2" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_white_cumulative_debt_2,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - More than one race - Cumulative debt" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_more_than_one_race_cumulative_debt,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - More than one race - Cumulative debt_2" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_more_than_one_race_cumulative_debt_2,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Other race or race not reported - Cumulative debt" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_other_race_or_race_not_reported_cumulative_debt,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Other race or race not reported - Cumulative debt_2" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_other_race_or_race_not_reported_cumulative_debt_2,
    "U.S. citizens and permanent residents - Ethnicity not reported - Other race or race not reported - Cumulative debt" AS u_s_citizens_and_permanent_residents_ethnicity_not_reported_other_race_or_race_not_reported_cumulative_debt,
    "U.S. citizens and permanent residents - Ethnicity not reported - Other race or race not reported - Cumulative debt_2" AS u_s_citizens_and_permanent_residents_ethnicity_not_reported_other_race_or_race_not_reported_cumulative_debt_2
FROM "ncses-nsf25349-tab004-005"
