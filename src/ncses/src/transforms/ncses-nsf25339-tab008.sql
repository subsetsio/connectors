-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "All federal obligations" AS all_federal_obligations,
    "R and D - Total" AS r_and_d_total,
    "R and D - Research" AS r_and_d_research,
    "R and D - Advanced technology development" AS r_and_d_advanced_technology_development,
    "R and D - Major systems development" AS r_and_d_major_systems_development,
    "R and D plant - Major systems development" AS r_and_d_plant_major_systems_development,
    "Facilities and equipment for instruction in S and E - Major systems development" AS facilities_and_equipment_for_instruction_in_s_and_e_major_systems_development,
    "S and E fellowships traineeships and training grants - Major systems development" AS s_and_e_fellowships_traineeships_and_training_grants_major_systems_development,
    "Other general support for S and E - Major systems development" AS other_general_support_for_s_and_e_major_systems_development
FROM "ncses-nsf25339-tab008"
