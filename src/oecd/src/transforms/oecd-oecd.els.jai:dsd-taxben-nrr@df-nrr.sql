-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "household_type",
    "age_children",
    "income_prev",
    "income_part",
    "unemp_duration",
    "soc_ass_benefit",
    "house_benefit",
    "freq",
    "obs_status",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.els.jai:dsd-taxben-nrr@df-nrr"
