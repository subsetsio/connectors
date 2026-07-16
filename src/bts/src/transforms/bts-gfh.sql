-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CARRIER" AS carrier,
    "CARRIER_ENTITY" AS carrier_entity,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH" AS BIGINT) AS month,
    "EXPENSE_TYPE" AS expense_type,
    "AIRCRAFT_TYPE" AS aircraft_type,
    CAST("AIRCRAFT_CONFIG" AS BIGINT) AS aircraft_config,
    CAST("EXP_PILOT_COPILOT" AS DOUBLE) AS exp_pilot_copilot,
    CAST("EXP_FUEL_OIL" AS DOUBLE) AS exp_fuel_oil,
    CAST("EXP_OTHER" AS DOUBLE) AS exp_other,
    CAST("EXP_MAINTENANCE" AS DOUBLE) AS exp_maintenance,
    CAST("EXP_DEPRECIATION" AS DOUBLE) AS exp_depreciation,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-gfh"
