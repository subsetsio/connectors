-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "SingaporeCitizens_Total" AS singaporecitizens_total,
    "SingaporeCitizens_Males" AS singaporecitizens_males,
    "SingaporeCitizens_Females" AS singaporecitizens_females,
    "PermanentResidents_Total" AS permanentresidents_total,
    "PermanentResidents_Males" AS permanentresidents_males,
    "PermanentResidents_Females" AS permanentresidents_females
FROM "sg-data-d-d455e3b51a0a58d9c85a937af90fdba0"
