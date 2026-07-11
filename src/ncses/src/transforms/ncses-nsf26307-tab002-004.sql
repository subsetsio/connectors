-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Detailed field" AS detailed_field,
    "Master's students - Total" AS master_s_students_total,
    "Master's students - Male - Number" AS master_s_students_male_number,
    "Master's students - Male - Percent" AS master_s_students_male_percent,
    "Master's students - Female - Number" AS master_s_students_female_number,
    "Master's students - Female - Percent" AS master_s_students_female_percent,
    "Doctoral students - Total - Percent" AS doctoral_students_total_percent,
    "Doctoral students - Male - Number" AS doctoral_students_male_number,
    "Doctoral students - Male - Percent" AS doctoral_students_male_percent,
    "Doctoral students - Female - Number" AS doctoral_students_female_number,
    "Doctoral students - Female - Percent" AS doctoral_students_female_percent,
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
FROM "ncses-nsf26307-tab002-004"
