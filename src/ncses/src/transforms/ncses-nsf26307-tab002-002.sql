-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Broad field" AS broad_field,
    "Graduate students - All graduate students - Total number" AS graduate_students_all_graduate_students_total_number,
    "Graduate students - All graduate students - Percentage in public institutions" AS graduate_students_all_graduate_students_percentage_in_public_institutions,
    "Graduate students - Master's - Total number" AS graduate_students_master_s_total_number,
    "Graduate students - Master's - Percentage in public institutions" AS graduate_students_master_s_percentage_in_public_institutions,
    "Graduate students - Doctoral - Total number" AS graduate_students_doctoral_total_number,
    "Graduate students - Doctoral - Percentage in public institutions" AS graduate_students_doctoral_percentage_in_public_institutions,
    "Postdoctoral appointees - Doctoral - Total number" AS postdoctoral_appointees_doctoral_total_number,
    "Postdoctoral appointees - Doctoral - Percentage in public institutions" AS postdoctoral_appointees_doctoral_percentage_in_public_institutions,
    "Doctorate-holding nonfaculty researchers - Doctoral - Total number" AS doctorate_holding_nonfaculty_researchers_doctoral_total_number,
    "Doctorate-holding nonfaculty researchers - Doctoral - Percentage in public institutions" AS doctorate_holding_nonfaculty_researchers_doctoral_percentage_in_public_institutions
FROM "ncses-nsf26307-tab002-002"
