-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "swd_ems_transports",
    "gen_ed_ems_transports",
    "total_ems_transports"
FROM "nyc-open-data-ftpm-ey3k"
