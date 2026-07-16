-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "AIRLINE_ID" AS airline_id,
    "UNIQUE_CARRIER" AS unique_carrier,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    "ENTITY" AS entity,
    CAST("GENERAL_MANAGE" AS BIGINT) AS general_manage,
    CAST("PILOTS_COPILOTS" AS BIGINT) AS pilots_copilots,
    CAST("OTHER_FLT_PERS" AS BIGINT) AS other_flt_pers,
    CAST("PASS_GEN_SVC_ADMIN" AS BIGINT) AS pass_gen_svc_admin,
    CAST("MAINTENANCE" AS BIGINT) AS maintenance,
    CAST("ARCFT_TRAF_HANDLING_GRP1" AS BIGINT) AS arcft_traf_handling_grp1,
    CAST("GEN_ARCFT_TRAF_HANDLING" AS BIGINT) AS gen_arcft_traf_handling,
    CAST("AIRCRAFT_CONTROL" AS BIGINT) AS aircraft_control,
    CAST("PASSENGER_HANDLING" AS BIGINT) AS passenger_handling,
    CAST("CARGO_HANDLING" AS BIGINT) AS cargo_handling,
    CAST("TRAINEES_INTRUCTOR" AS BIGINT) AS trainees_intructor,
    CAST("STATISTICAL" AS BIGINT) AS statistical,
    CAST("TRAFFIC_SOLICITERS" AS BIGINT) AS traffic_soliciters,
    CAST("OTHER" AS BIGINT) AS other,
    CAST("TRANSPORT_RELATED" AS BIGINT) AS transport_related,
    CAST("TOTAL" AS BIGINT) AS total,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-gdf"
