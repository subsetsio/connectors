-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH" AS BIGINT) AS month,
    CAST("AIRLINE_ID" AS BIGINT) AS airline_id,
    "UNIQUE_CARRIER" AS unique_carrier,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    CAST("CARRIER_GROUP" AS BIGINT) AS carrier_group,
    CAST("CARRIER_GROUP_NEW" AS BIGINT) AS carrier_group_new,
    CAST("EMPFULL" AS BIGINT) AS empfull,
    CAST("EMPPART" AS BIGINT) AS emppart,
    CAST("EMPTOTAL" AS BIGINT) AS emptotal,
    CAST("EMPFTE" AS BIGINT) AS empfte,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-gef"
