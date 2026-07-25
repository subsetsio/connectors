-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    "Terson_UrbanRural" AS terson_urbanrural,
    "P04_Gender_ID" AS p04_gender_id,
    "Terson_Parent" AS terson_parent,
    CAST("time" AS BIGINT) AS time,
    CAST("value" AS BIGINT) AS value
FROM "rosstat-7708234640-vpn2021"
