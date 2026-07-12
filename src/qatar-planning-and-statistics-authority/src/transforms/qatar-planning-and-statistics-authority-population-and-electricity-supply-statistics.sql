-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population",
    "population_annual_increase",
    "total_energy_generation_inlcuding_all_auxilliary_consumption_gwh",
    "energy_transmitted_sent_out_gwh_generation_minus_auxilliary_consumption",
    "electricity_net_distribution_gwh_injected_generation_minus_real_losses",
    "electricity_consumption_gwh_excluding_bulk_industrial"
FROM "qatar-planning-and-statistics-authority-population-and-electricity-supply-statistics"
