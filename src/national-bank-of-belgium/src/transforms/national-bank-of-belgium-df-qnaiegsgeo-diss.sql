-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "TYPE" AS type,
    "IE" AS ie,
    "ITEM" AS item,
    "ADJUSTMENT" AS adjustment,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status,
    "CONF_STATUS" AS conf_status,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "national-bank-of-belgium-df-qnaiegsgeo-diss"
