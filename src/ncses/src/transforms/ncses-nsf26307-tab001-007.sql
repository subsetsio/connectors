-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "Graduate students - Total" AS graduate_students_total,
    "Graduate students - U.S. citizens and permanent residents - Number" AS graduate_students_u_s_citizens_and_permanent_residents_number,
    "Graduate students - U.S. citizens and permanent residents - Percent" AS graduate_students_u_s_citizens_and_permanent_residents_percent,
    "Graduate students - Temporary visa holders - Number" AS graduate_students_temporary_visa_holders_number,
    "Graduate students - Temporary visa holders - Percent" AS graduate_students_temporary_visa_holders_percent,
    "Postdoctoral appointees - Total - Percent" AS postdoctoral_appointees_total_percent,
    "Postdoctoral appointees - U.S. citizens and permanent residents - Number" AS postdoctoral_appointees_u_s_citizens_and_permanent_residents_number,
    "Postdoctoral appointees - U.S. citizens and permanent residents - Percent" AS postdoctoral_appointees_u_s_citizens_and_permanent_residents_percent,
    "Postdoctoral appointees - Temporary visa holders - Number" AS postdoctoral_appointees_temporary_visa_holders_number,
    "Postdoctoral appointees - Temporary visa holders - Percent" AS postdoctoral_appointees_temporary_visa_holders_percent
FROM "ncses-nsf26307-tab001-007"
