-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PRITRA: Prices & Transformation" AS pritra_prices_transformation,
    "ACCOUNTING_ENTRY: Accounting entry" AS accounting_entry_accounting_entry,
    "SECTOR: Sector" AS sector_sector,
    "MEASURE: Measure" AS measure_measure,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "DECIMALS: Decimals" AS decimals_decimals,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier
FROM "statec-df-e2220"
