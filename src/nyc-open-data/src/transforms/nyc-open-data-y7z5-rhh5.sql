-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_quarter",
    "facility_name",
    "provider_agency",
    "performance_tier"
FROM "nyc-open-data-y7z5-rhh5"
