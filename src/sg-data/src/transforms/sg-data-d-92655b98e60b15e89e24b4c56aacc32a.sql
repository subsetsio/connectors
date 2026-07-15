-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Owner_Occupied" AS total_owner_occupied,
    "Total_Rented" AS total_rented,
    "Total_Others" AS total_others,
    "Chinese_Total" AS chinese_total,
    "Chinese_Owner_Occupied" AS chinese_owner_occupied,
    "Chinese_Rented" AS chinese_rented,
    "Chinese_Others" AS chinese_others,
    "Malays_Total" AS malays_total,
    "Malays_Owner_Occupied" AS malays_owner_occupied,
    "Malays_Rented" AS malays_rented,
    "Malays_Others" AS malays_others,
    "Indians_Total" AS indians_total,
    "Indians_Owner_Occupied" AS indians_owner_occupied,
    "Indians_Rented" AS indians_rented,
    "Indians_Others" AS indians_others,
    "Others_Total" AS others_total,
    "Others_Owner_Occupied" AS others_owner_occupied,
    "Others_Rented" AS others_rented,
    "Others_Others" AS others_others
FROM "sg-data-d-92655b98e60b15e89e24b4c56aacc32a"
