-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "based_on_total_energy_generation_ipps_including_auxilliary_consumption",
    "based_on_energy_sent_out_net_ipps_generation",
    "based_on_electricity_net_distribution",
    "based_on_electricity_net_distribution_excluding_industrial_bulk_consumers"
FROM "qatar-planning-and-statistics-authority-per-capita-electricity-consumption-by-method-of-calculation"
