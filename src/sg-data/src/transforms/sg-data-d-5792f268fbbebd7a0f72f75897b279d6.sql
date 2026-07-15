-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Chinese" AS total_chinese,
    "Total_Malays" AS total_malays,
    "Total_Indians" AS total_indians,
    "Total_Others" AS total_others,
    "EconomicallyActive_Total" AS economicallyactive_total,
    "EconomicallyActive_Chinese" AS economicallyactive_chinese,
    "EconomicallyActive_Malays" AS economicallyactive_malays,
    "EconomicallyActive_Indians" AS economicallyactive_indians,
    "EconomicallyActive_Others" AS economicallyactive_others,
    "EconomicallyInactive_Total" AS economicallyinactive_total,
    "EconomicallyInactive_Chinese" AS economicallyinactive_chinese,
    "EconomicallyInactive_Malays" AS economicallyinactive_malays,
    "EconomicallyInactive_Indians" AS economicallyinactive_indians,
    "EconomicallyInactive_Others" AS economicallyinactive_others
FROM "sg-data-d-5792f268fbbebd7a0f72f75897b279d6"
