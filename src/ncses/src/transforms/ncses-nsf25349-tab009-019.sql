-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Characteristic" AS characteristic,
    "Totala" AS totala,
    "U.S. citizen" AS u_s_citizen,
    "Temporary visa holder" AS temporary_visa_holder,
    "Hispanic or Latino - U.S. citizen" AS hispanic_or_latino_u_s_citizen,
    "Hispanic or Latino - Temporary visa holder" AS hispanic_or_latino_temporary_visa_holder,
    "Not Hispanic or Latino - American Indian or Alaska Native - U.S. citizen" AS not_hispanic_or_latino_american_indian_or_alaska_native_u_s_citizen,
    "Not Hispanic or Latino - American Indian or Alaska Native - Temporary visa holder" AS not_hispanic_or_latino_american_indian_or_alaska_native_temporary_visa_holder,
    "Not Hispanic or Latino - Asian - U.S. citizen" AS not_hispanic_or_latino_asian_u_s_citizen,
    "Not Hispanic or Latino - Asian - Temporary visa holder" AS not_hispanic_or_latino_asian_temporary_visa_holder,
    "Not Hispanic or Latino - Black or African American - U.S. citizen" AS not_hispanic_or_latino_black_or_african_american_u_s_citizen,
    "Not Hispanic or Latino - Black or African American - Temporary visa holder" AS not_hispanic_or_latino_black_or_african_american_temporary_visa_holder,
    "Not Hispanic or Latino - White - U.S. citizen" AS not_hispanic_or_latino_white_u_s_citizen,
    "Not Hispanic or Latino - White - Temporary visa holder" AS not_hispanic_or_latino_white_temporary_visa_holder,
    "Not Hispanic or Latino - More than one race - U.S. citizen" AS not_hispanic_or_latino_more_than_one_race_u_s_citizen,
    "Not Hispanic or Latino - More than one race - Temporary visa holder" AS not_hispanic_or_latino_more_than_one_race_temporary_visa_holder,
    "Not Hispanic or Latino - Other race or race not reported - U.S. citizen" AS not_hispanic_or_latino_other_race_or_race_not_reported_u_s_citizen,
    "Not Hispanic or Latino - Other race or race not reported - Temporary visa holder" AS not_hispanic_or_latino_other_race_or_race_not_reported_temporary_visa_holder,
    "Ethnicity not reported - Other race or race not reported - U.S. citizen" AS ethnicity_not_reported_other_race_or_race_not_reported_u_s_citizen,
    "Ethnicity not reported - Other race or race not reported - Temporary visa holder" AS ethnicity_not_reported_other_race_or_race_not_reported_temporary_visa_holder
FROM "ncses-nsf25349-tab009-019"
