-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "REPORTING" AS reporting,
    "COUNTRY" AS country,
    "PRODUCT" AS product,
    "FLOW" AS flow,
    "CONCEPT" AS concept,
    "DATATYPE" AS datatype,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "OBS_STATUS" AS obs_status,
    "CONF_STATUS" AS conf_status,
    "UNIT_MEASURE" AS unit_measure,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "EMBARGO_TIME" AS embargo_time,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "national-bank-of-belgium-df-exttradevlnat-overview"
