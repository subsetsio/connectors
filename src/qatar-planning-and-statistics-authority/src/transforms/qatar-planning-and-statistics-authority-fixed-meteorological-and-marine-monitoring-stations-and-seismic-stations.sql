-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no_of_meteorological_stations",
    "no_of_marine_buoys_fixed_marine_monitoring_stations",
    "no_of_seismic_stations"
FROM "qatar-planning-and-statistics-authority-fixed-meteorological-and-marine-monitoring-stations-and-seismic-stations"
