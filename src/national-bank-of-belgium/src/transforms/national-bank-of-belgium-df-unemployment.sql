-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "BE_REGION" AS be_region,
    "GENDER" AS gender,
    "INACTIVITY" AS inactivity,
    "AGE" AS age,
    CAST("EDUCATION" AS BIGINT) AS education,
    "ACTIVITY" AS activity,
    "SERVICES" AS services,
    "NATIONALITY" AS nationality,
    "ADJUSTMENT" AS adjustment,
    "PROF_GROUP" AS prof_group,
    CAST("EMPLOY_CATEGORY" AS BIGINT) AS employ_category,
    "INDEX_TYPE" AS index_type,
    "DERIVATION" AS derivation,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "OBS_STATUS" AS obs_status,
    "UNIT_MEASURE" AS unit_measure,
    "UNIT_MULT" AS unit_mult,
    "COMPILING_ORG" AS compiling_org,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "national-bank-of-belgium-df-unemployment"
