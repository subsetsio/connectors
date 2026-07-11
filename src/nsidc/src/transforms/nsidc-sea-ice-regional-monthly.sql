-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are monthly sub-basin observations; do not aggregate them with the daily regional table without accounting for the different temporal aggregation.
SELECT
    "hemisphere",
    "region",
    "year",
    "month",
    "date",
    "area_sq_km",
    "area_rank",
    "extent_sq_km",
    "extent_rank"
FROM "nsidc-sea-ice-regional-monthly"
