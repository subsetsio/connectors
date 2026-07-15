-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Chinese_Total" AS chinese_total,
    "Chinese_Males" AS chinese_males,
    "Chinese_Females" AS chinese_females,
    "Malays_Total" AS malays_total,
    "Malays_Males" AS malays_males,
    "Malays_Females" AS malays_females,
    "Indians_Total" AS indians_total,
    "Indians_Males" AS indians_males,
    "Indians_Females" AS indians_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-b082ea2b88b610aefa402e7f7e1475a2"
