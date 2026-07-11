-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Country names and reactor attributes reflect PRIS reactor metadata as published for each unit; use the PRIS reactor_id as the stable join key to annual performance rows.
SELECT
    "reactor_id",
    "name",
    "alternate_name",
    "country",
    "country_code",
    "status",
    "reactor_type",
    "model",
    "reference_unit_power_mwe",
    "design_net_capacity_mwe",
    "gross_capacity_mwe",
    "thermal_capacity_mwt",
    strptime("construction_start_date", '%Y-%m-%d')::DATE AS construction_start_date,
    strptime("first_criticality_date", '%Y-%m-%d')::DATE AS first_criticality_date,
    strptime("first_grid_connection_date", '%Y-%m-%d')::DATE AS first_grid_connection_date,
    strptime("commercial_operation_date", '%Y-%m-%d')::DATE AS commercial_operation_date,
    strptime("long_term_shutdown_date", '%Y-%m-%d')::DATE AS long_term_shutdown_date,
    strptime("permanent_shutdown_date", '%Y-%m-%d')::DATE AS permanent_shutdown_date,
    "lifetime_electricity_supplied_twh",
    "lifetime_operation_factor_pct",
    "lifetime_energy_availability_factor_pct",
    "lifetime_load_factor_pct"
FROM "iaea-pris-reactors"
