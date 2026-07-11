-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "Graduate students - Total" AS graduate_students_total,
    "Graduate students - Male - Number" AS graduate_students_male_number,
    "Graduate students - Male - Percent" AS graduate_students_male_percent,
    "Graduate students - Female - Number" AS graduate_students_female_number,
    "Graduate students - Female - Percent" AS graduate_students_female_percent,
    "Postdoctoral appointees - Total - Percent" AS postdoctoral_appointees_total_percent,
    "Postdoctoral appointees - Male - Number" AS postdoctoral_appointees_male_number,
    "Postdoctoral appointees - Male - Percent" AS postdoctoral_appointees_male_percent,
    "Postdoctoral appointees - Female - Number" AS postdoctoral_appointees_female_number,
    "Postdoctoral appointees - Female - Percent" AS postdoctoral_appointees_female_percent,
    "Doctorate-holding nonfaculty researchers - Total - Percent" AS doctorate_holding_nonfaculty_researchers_total_percent,
    "Doctorate-holding nonfaculty researchers - Male - Number" AS doctorate_holding_nonfaculty_researchers_male_number,
    "Doctorate-holding nonfaculty researchers - Male - Percent" AS doctorate_holding_nonfaculty_researchers_male_percent,
    "Doctorate-holding nonfaculty researchers - Female - Number" AS doctorate_holding_nonfaculty_researchers_female_number,
    "Doctorate-holding nonfaculty researchers - Female - Percent" AS doctorate_holding_nonfaculty_researchers_female_percent
FROM "ncses-nsf26307-tab001-006"
