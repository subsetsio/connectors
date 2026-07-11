-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Broad field" AS broad_field,
    "Total - Number" AS total_number,
    "Total - Percent" AS total_percent,
    "U.S. citizens and permanent residents - Hispanic or Latino - Number" AS u_s_citizens_and_permanent_residents_hispanic_or_latino_number,
    "U.S. citizens and permanent residents - Hispanic or Latino - Percent" AS u_s_citizens_and_permanent_residents_hispanic_or_latino_percent,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - American Indian or Alaska Native - Number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_american_indian_or_alaska_native_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - American Indian or Alaska Native - Percent" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_american_indian_or_alaska_native_percent,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Asian - Number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_asian_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Asian - Percent" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_asian_percent,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Black or African American - Number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_black_or_african_american_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Black or African American - Percent" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_black_or_african_american_percent,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Native Hawaiian or Other Pacific Islander - Number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_native_hawaiian_or_other_pacific_islander_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - Native Hawaiian or Other Pacific Islander - Percent" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_native_hawaiian_or_other_pacific_islander_percent,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - White - Number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_white_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - White - Percent" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_white_percent,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - More than one race - Number" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_more_than_one_race_number,
    "U.S. citizens and permanent residents - Not Hispanic or Latino - More than one race - Percent" AS u_s_citizens_and_permanent_residents_not_hispanic_or_latino_more_than_one_race_percent,
    "U.S. citizens and permanent residents - Unknown ethnicity and race - More than one race - Number" AS u_s_citizens_and_permanent_residents_unknown_ethnicity_and_race_more_than_one_race_number,
    "U.S. citizens and permanent residents - Unknown ethnicity and race - More than one race - Percent" AS u_s_citizens_and_permanent_residents_unknown_ethnicity_and_race_more_than_one_race_percent,
    "Temporary visa holders - Unknown ethnicity and race - More than one race - Number" AS temporary_visa_holders_unknown_ethnicity_and_race_more_than_one_race_number,
    "Temporary visa holders - Unknown ethnicity and race - More than one race - Percent" AS temporary_visa_holders_unknown_ethnicity_and_race_more_than_one_race_percent
FROM "ncses-nsf26307-tab002-009"
