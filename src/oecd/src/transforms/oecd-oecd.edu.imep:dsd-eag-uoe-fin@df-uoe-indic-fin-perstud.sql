-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "education_lev",
    "exp_source",
    "exp_destination",
    "expenditure_type",
    "price_base",
    "unit_measure",
    "q_sheet",
    "obs_status",
    "obs_status_2",
    "obs_status_3",
    "unit_mult",
    "decimals",
    "base_per",
    "q_sheet_row_id",
    "last_update",
    "last_modified",
    "numerator_category",
    "numerator_value",
    "denominator_category",
    "denominator_value",
    "time_period",
    "value"
FROM "oecd-oecd.edu.imep:dsd-eag-uoe-fin@df-uoe-indic-fin-perstud"
