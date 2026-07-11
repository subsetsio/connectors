-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "REF_SECTOR" AS ref_sector,
    "COUNTERPART_SECTOR" AS counterpart_sector,
    "ACCOUNTING_ENTRY" AS accounting_entry,
    "IIP_ITEM" AS iip_item,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value,
    "OBS_STATUS" AS obs_status,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "national-bank-of-belgium-df-iip"
