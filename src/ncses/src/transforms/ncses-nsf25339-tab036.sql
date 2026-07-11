-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Consortium" AS consortium,
    "All federal obligations" AS all_federal_obligations,
    "R and D" AS r_and_d,
    "R and D plant" AS r_and_d_plant,
    "Facilities and equipment for instruction in S and E" AS facilities_and_equipment_for_instruction_in_s_and_e,
    "S and E fellowships traineeships and training grants" AS s_and_e_fellowships_traineeships_and_training_grants,
    "Other general support for S and E" AS other_general_support_for_s_and_e
FROM "ncses-nsf25339-tab036"
