-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "asset_allocation_in_millions",
    "teachers",
    "nycers",
    "police",
    "fire",
    "bers",
    "total",
    "report_year",
    "report_month"
FROM "nyc-open-data-rh3d-kgz3"
