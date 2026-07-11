-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Detailed field" AS detailed_field,
    "Graduate students - All graduate students - Number" AS graduate_students_all_graduate_students_number,
    "Graduate students - All graduate students - Percent" AS graduate_students_all_graduate_students_percent,
    "Graduate students - Master's - Number" AS graduate_students_master_s_number,
    "Graduate students - Master's - Percent" AS graduate_students_master_s_percent,
    "Graduate students - Doctoral - Number" AS graduate_students_doctoral_number,
    "Graduate students - Doctoral - Percent" AS graduate_students_doctoral_percent,
    "Postdoctoral appointees - Doctoral - Number" AS postdoctoral_appointees_doctoral_number,
    "Postdoctoral appointees - Doctoral - Percent" AS postdoctoral_appointees_doctoral_percent,
    "Doctorate-holding nonfaculty researchers - Doctoral - Number" AS doctorate_holding_nonfaculty_researchers_doctoral_number,
    "Doctorate-holding nonfaculty researchers - Doctoral - Percent" AS doctorate_holding_nonfaculty_researchers_doctoral_percent
FROM "ncses-nsf26307-tab002-001"
