-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains multiple commodities, energy transactions, units, and reference areas; filter unit and transaction dimensions before aggregating values.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "REF_AREA" AS ref_area,
    "COMMODITY" AS commodity,
    "TRANSACTION" AS transaction,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT" AS unit_mult,
    "UNIT_MEASURE" AS unit_measure,
    "OBS_STATUS" AS obs_status,
    "CONVERSION_FACTOR" AS conversion_factor
FROM "un-statistics-division-df-undata-energy"
