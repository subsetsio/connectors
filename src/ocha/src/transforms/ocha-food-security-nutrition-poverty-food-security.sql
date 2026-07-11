-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix IPC phases and administrative levels; filter ipc_phase and admin_level before aggregating population_in_phase or fractions.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "resource_hdx_id",
    "ipc_phase",
    "ipc_type",
    "population_in_phase",
    "population_fraction_in_phase",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-food-security-nutrition-poverty-food-security"
