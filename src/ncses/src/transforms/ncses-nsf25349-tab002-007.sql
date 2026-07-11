-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Employment commitment sector and year - All U.S. employment commitments number" AS employment_commitment_sector_and_year_all_u_s_employment_commitments_number,
    "Totala - All U.S. employment commitments number" AS totala_all_u_s_employment_commitments_number,
    "Sex - Male - All U.S. employment commitments number" AS sex_male_all_u_s_employment_commitments_number,
    "Sex - Female - All U.S. employment commitments number" AS sex_female_all_u_s_employment_commitments_number,
    "Citizenship status - U.S. citizen or permanent resident - All U.S. employment commitments number" AS citizenship_status_u_s_citizen_or_permanent_resident_all_u_s_employment_commitments_number,
    "Citizenship status - Temporary visa holder - All U.S. employment commitments number" AS citizenship_status_temporary_visa_holder_all_u_s_employment_commitments_number,
    "U.S. citizens and permanent residents - Hispanic or Latino - Temporary visa holder - All U.S. employment commitments number" AS u_s_citizens_and_permanent_residents_hispanic_or_latino_temporary_visa_holder_all_u_s_employment_commitments_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - American Indian or Alaska Native - All U.S. employment commitments number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_american_indian_or_alaska_native_all_u_s_employment_commitments_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Asianb - All U.S. employment commitments number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_asianb_all_u_s_employment_commitments_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Black or African American - All U.S. employment commitments number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_black_or_african_american_all_u_s_employment_commitments_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - White - All U.S. employment commitments number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_white_all_u_s_employment_commitments_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - More than one race - All U.S. employment commitments number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_more_than_one_race_all_u_s_employment_commitments_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Other race or race not reportedc - All U.S. employment commitments number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_other_race_or_race_not_reportedc_all_u_s_employment_commitments_number,
    "U.S. citizens and permanent residents - Ethnicity not reported - Other race or race not reportedc - All U.S. employment commitments number" AS u_s_citizens_and_permanent_residents_ethnicity_not_reported_other_race_or_race_not_reportedc_all_u_s_employment_commitments_number
FROM "ncses-nsf25349-tab002-007"
