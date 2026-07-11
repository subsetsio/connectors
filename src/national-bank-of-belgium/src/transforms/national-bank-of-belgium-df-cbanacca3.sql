-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "SECTOR" AS sector,
    "AMNR" AS amnr,
    "CBANACCA3_ITEM" AS cbanacca3_item,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value,
    "OBS_STATUS" AS obs_status,
    "UNIT_MEASURE" AS unit_measure,
    "UNIT_MULT" AS unit_mult,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "national-bank-of-belgium-df-cbanacca3"
