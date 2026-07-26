-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "system_code",
    "location_name",
    "location_category_description",
    "administrative_district_code",
    "principal",
    "removal",
    "superintendent",
    "total_removalssuspensions",
    "expulsions"
FROM "nyc-open-data-vzuc-vmd8"
