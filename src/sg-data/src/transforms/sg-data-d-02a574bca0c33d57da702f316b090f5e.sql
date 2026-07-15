-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Owner" AS total_owner,
    "Total_Non_Owner" AS total_non_owner,
    "Chinese_Total" AS chinese_total,
    "Chinese_Owner" AS chinese_owner,
    "Chinese_Non_Owner" AS chinese_non_owner,
    "Malays_Total" AS malays_total,
    "Malays_Owner" AS malays_owner,
    "Malays_Non_Owner" AS malays_non_owner,
    "Indians_Total" AS indians_total,
    "Indians_Owner" AS indians_owner,
    "Indians_Non_Owner" AS indians_non_owner,
    "Others_Total" AS others_total,
    "Others_Owner" AS others_owner,
    "Others_Non_Owner" AS others_non_owner
FROM "sg-data-d-02a574bca0c33d57da702f316b090f5e"
