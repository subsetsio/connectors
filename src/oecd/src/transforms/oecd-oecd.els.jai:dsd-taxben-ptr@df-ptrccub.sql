-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "income_curr",
    "household_type",
    "age_children",
    "income_part",
    "childcare_use",
    "unemp_duration",
    "soc_ass_benefit",
    "house_benefit",
    "temp_intowork_benefit",
    "benefit_type",
    "contribution",
    "freq",
    "obs_status",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.els.jai:dsd-taxben-ptr@df-ptrccub"
