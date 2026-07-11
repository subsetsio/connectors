-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "price_base",
    "unit_measure",
    "q_sheet",
    "obs_status",
    "obs_status_2",
    "obs_status_3",
    "unit_mult",
    "decimals",
    "base_per",
    "last_update",
    "last_modified",
    "source_data",
    "time_period",
    "value"
FROM "oecd-oecd.edu.imep:dsd-eag-uoe-fin-annex@df-uoe-fin-annex"
