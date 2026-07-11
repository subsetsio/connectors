-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State and outlying area - All states and outlying areas" AS state_and_outlying_area_all_states_and_outlying_areas,
    "All federal obligations - All states and outlying areas" AS all_federal_obligations_all_states_and_outlying_areas,
    "R and D - All states and outlying areas" AS r_and_d_all_states_and_outlying_areas,
    "R and D plant - All states and outlying areas" AS r_and_d_plant_all_states_and_outlying_areas,
    "Facilities and equipment for instruction in S and E - All states and outlying areas" AS facilities_and_equipment_for_instruction_in_s_and_e_all_states_and_outlying_areas,
    "S and E fellowships traineeships and training grants - All states and outlying areas" AS s_and_e_fellowships_traineeships_and_training_grants_all_states_and_outlying_areas,
    "Other general support for S and E - All states and outlying areas" AS other_general_support_for_s_and_e_all_states_and_outlying_areas
FROM "ncses-nsf25339-tab009"
