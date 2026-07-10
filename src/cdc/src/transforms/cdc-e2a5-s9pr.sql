-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Case_status" AS case_status,
    "Sex" AS sex,
    "Age_cat_yrs" AS age_cat_yrs,
    "Race" AS race,
    "Ethnicity" AS ethnicity,
    "Onset_month" AS onset_month,
    "EM" AS em,
    "Arthritis" AS arthritis,
    "Facial_palsy" AS facial_palsy,
    "Radiculo" AS radiculo,
    "Lymph_men" AS lymph_men,
    "Enceph" AS enceph,
    "Av_block" AS av_block
FROM "cdc-e2a5-s9pr"
