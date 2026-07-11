-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "freq",
    "period",
    "measure",
    "activity",
    "product",
    "dd_dim",
    "dd_id",
    "obs_status",
    "conf_status",
    "value"
FROM "oecd-oecd.sdd.sdps:dsd-dd-hcl@df-dd-hcl-test"
