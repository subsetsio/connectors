-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "REF_AREA" AS ref_area,
    "ACCOUNTING_ENTRY" AS accounting_entry,
    "PRICES" AS prices,
    "FREQ" AS freq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "COUNTERPART_AREA" AS counterpart_area,
    "UNIT_MEASURE" AS unit_measure,
    "VALUATION" AS valuation,
    "ACTIVITY" AS activity,
    "STO" AS sto,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-comptes-regionaux"
