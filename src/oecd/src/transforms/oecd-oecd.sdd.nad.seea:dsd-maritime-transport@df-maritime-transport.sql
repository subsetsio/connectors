-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "freq",
    "measure",
    "unit_measure",
    "adjustment",
    "pollutant",
    "methodology",
    "source",
    "vessel",
    "vessel_emissions_source",
    "obs_status",
    "unit_mult",
    "classification",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.nad.seea:dsd-maritime-transport@df-maritime-transport"
