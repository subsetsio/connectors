-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are monthly averages; do not combine this table with daily observations without accounting for the different temporal aggregation.
SELECT
    "hemisphere",
    "year",
    "month",
    "date",
    "source_dataset",
    "extent_million_sq_km",
    "area_million_sq_km"
FROM "nsidc-sea-ice-extent-monthly"
