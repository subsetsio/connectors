-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Energy balance data include multiple commodities, balance transactions, countries, and units; filter those dimensions before aggregating.
SELECT
    "DATAFLOW" AS dataflow,
    "REF_AREA" AS ref_area,
    "COMMODITY" AS commodity,
    "TRANSACTION" AS transaction,
    "UNIT" AS unit,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "ESTIMATE" AS estimate,
    "FOOTNOTES" AS footnotes,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult
FROM "undata-df-undata-energybalance"
