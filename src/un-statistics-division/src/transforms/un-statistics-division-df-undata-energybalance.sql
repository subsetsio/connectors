-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains energy balance observations by commodity, transaction, unit, reference area, and year; avoid summing across unit or transaction categories.
SELECT
    "DATAFLOW" AS dataflow,
    "REF_AREA" AS ref_area,
    "COMMODITY" AS commodity,
    "TRANSACTION" AS transaction,
    "UNIT" AS unit,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "ESTIMATE" AS estimate,
    "FOOTNOTES" AS footnotes,
    "UNIT_MULT" AS unit_mult
FROM "un-statistics-division-df-undata-energybalance"
