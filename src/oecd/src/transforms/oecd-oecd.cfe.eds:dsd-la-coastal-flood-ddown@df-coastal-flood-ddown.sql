-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "dd_id",
    "ref_area",
    "measure",
    "unit_measure",
    "ret_period",
    "territorial_level",
    "territorial_type",
    "dd_dim",
    "freq",
    "obs_status",
    "decimals",
    "local_area_name",
    "time_period",
    "value"
FROM "oecd-oecd.cfe.eds:dsd-la-coastal-flood-ddown@df-coastal-flood-ddown"
