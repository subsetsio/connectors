-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "measure",
    "final_demand_area",
    "emissions_origin_area",
    "emissions_origin_activity",
    "unit_measure",
    "unit_mult",
    "time_period",
    "value"
FROM "oecd-oecd.sti.pie:dsd-icio-ghg-orgn-2025@df-icio-ghg-orgn-2025"
