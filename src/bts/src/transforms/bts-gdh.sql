-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("AIRLINE_ID" AS BIGINT) AS airline_id,
    "CARRIER" AS carrier,
    "CARRIER_ENTITY" AS carrier_entity,
    "CARRIER_NAME" AS carrier_name,
    "UNIQUE_CARRIER" AS unique_carrier,
    "UNIQUE_CARRIER_ENTITY" AS unique_carrier_entity,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    CAST("WAC" AS BIGINT) AS wac,
    CAST("CARRIER_GROUP" AS BIGINT) AS carrier_group,
    CAST("CARRIER_GROUP_NEW" AS BIGINT) AS carrier_group_new,
    "REGION" AS region,
    "START_DATE_SOURCE" AS start_date_source,
    "THRU_DATE_SOURCE" AS thru_date_source
FROM "bts-gdh"
