-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "FDI_ACCOUNT" AS fdi_account,
    "FDI_BALANCE" AS fdi_balance,
    "FDI_DIRECTION" AS fdi_direction,
    "FDI_ITEM" AS fdi_item,
    "FDI_AREA" AS fdi_area,
    "FDI_SECTOR" AS fdi_sector,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT" AS unit_mult,
    "OBS_STATUS" AS obs_status,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "national-bank-of-belgium-df-fdi-al"
