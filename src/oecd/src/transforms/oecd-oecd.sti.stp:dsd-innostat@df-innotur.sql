-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "activity",
    "size_class",
    "rd",
    "inno_type",
    "inno_empdist",
    "report_year",
    "obs_status",
    "obs_status_2",
    "unit_mult",
    "freq",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.sti.stp:dsd-innostat@df-innotur"
