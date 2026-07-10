-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Energy statistics include multiple commodities, transactions, countries, and units; filter commodity, transaction, and unit before aggregating.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "REF_AREA" AS ref_area,
    "COMMODITY" AS commodity,
    "TRANSACTION" AS transaction,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "UNIT_MEASURE" AS unit_measure,
    "OBS_STATUS" AS obs_status,
    CAST("CONVERSION_FACTOR" AS DOUBLE) AS conversion_factor
FROM "undata-df-undata-energy"
