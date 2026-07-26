-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "removals",
    "principal",
    "superintendent",
    "expulsions",
    "sy1718_total_removalssuspensions"
FROM "nyc-open-data-4e9g-bgra"
