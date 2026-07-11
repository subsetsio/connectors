-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "activity",
    "pol_cat",
    "measure",
    "unit_measure",
    "explanatory_notes",
    "leg_prov",
    "off_sources",
    "unoff_sources",
    "link_sources",
    "eu_ex",
    "saf",
    "restriction_status",
    "measure_id",
    "decimals",
    "unit_mult",
    "obs_status",
    "time_period",
    "value"
FROM "oecd-oecd.daf.inv:dsd-fdirri-reg-database@df-fdirri-reg-database"
