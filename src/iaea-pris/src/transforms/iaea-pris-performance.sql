-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is an annual observation for one reactor; join to iaea-pris-reactors on reactor_id before aggregating by country, reactor type, or status.
SELECT
    "reactor_id",
    "year",
    "electricity_supplied_gwh",
    "reference_unit_power_mw",
    "annual_time_on_line_h",
    "operation_factor_pct",
    "energy_availability_factor_pct",
    "load_factor_pct"
FROM "iaea-pris-performance"
