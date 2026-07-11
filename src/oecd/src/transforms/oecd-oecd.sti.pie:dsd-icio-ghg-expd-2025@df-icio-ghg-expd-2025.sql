-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "measure",
    "final_demand_area",
    "activity",
    "final_demand_category",
    "unit_measure",
    "unit_mult",
    "time_period",
    "value"
FROM "oecd-oecd.sti.pie:dsd-icio-ghg-expd-2025@df-icio-ghg-expd-2025"
