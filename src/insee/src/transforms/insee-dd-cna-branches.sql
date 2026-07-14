-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: National accounts datacubes contain multiple accounting concepts, sectors, transformations, price bases, and units in one long table; filter the relevant dimensions before aggregating observations.
SELECT
    "TRANSFORMATION" AS transformation,
    "PRICES" AS prices,
    "EXPENDITURE" AS expenditure,
    "STO" AS sto,
    "ACCOUNTING_ENTRY" AS accounting_entry,
    "PRODUCT" AS product,
    "FREQ" AS freq,
    "REF_SECTOR" AS ref_sector,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "COUNTERPART_AREA" AS counterpart_area,
    "UNIT_MEASURE" AS unit_measure,
    "INSTR_ASSET" AS instr_asset,
    "ACTIVITY" AS activity,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-dd-cna-branches"
