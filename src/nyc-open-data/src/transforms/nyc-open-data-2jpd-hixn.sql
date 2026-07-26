-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "administrative_district_code",
    "principal",
    "removal",
    "superintendent",
    "total_removalssuspensions"
FROM "nyc-open-data-2jpd-hixn"
