-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("operator_id" AS BIGINT) AS operator_id,
    "operator_name",
    "op_strcity",
    "op_state",
    "op_strzip",
    "op_country",
    "url",
    CAST("federal_state_local" AS BOOLEAN) AS federal_state_local,
    CAST("ticket_revenue" AS BIGINT) AS ticket_revenue,
    CAST("private_contract_revenue" AS DOUBLE) AS private_contract_revenue,
    CAST("advertising_revenue" AS DOUBLE) AS advertising_revenue,
    CAST("public_contract_revenue" AS DOUBLE) AS public_contract_revenue,
    CAST("federal_funding_revenue" AS DOUBLE) AS federal_funding_revenue,
    CAST("state_funding_revenue" AS DOUBLE) AS state_funding_revenue,
    CAST("local_funding_revenue" AS DOUBLE) AS local_funding_revenue,
    CAST("other_funding_revenue" AS DOUBLE) AS other_funding_revenue,
    CAST("trip_purpose_commuter_transit" AS BOOLEAN) AS trip_purpose_commuter_transit,
    CAST("trip_purpose_emergency" AS BOOLEAN) AS trip_purpose_emergency,
    CAST("trip_purpose_lifeline" AS BOOLEAN) AS trip_purpose_lifeline,
    CAST("trip_purpose_nps" AS BOOLEAN) AS trip_purpose_nps,
    CAST("trip_purpose_other" AS BOOLEAN) AS trip_purpose_other,
    "trip_purpose_other_desc",
    CAST("trip_purpose_pleasure" AS BOOLEAN) AS trip_purpose_pleasure,
    CAST("trip_purpose_roadway_conn" AS BOOLEAN) AS trip_purpose_roadway_conn,
    CAST("accepts_public_funding" AS BOOLEAN) AS accepts_public_funding,
    CAST("census_year" AS BIGINT) AS census_year
FROM "u-s-department-of-transportation-qzhh-3xej"
