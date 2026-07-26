-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zip_code",
    "building_type_service_class",
    "consumption_therms",
    "consumption_gj",
    "utilitydata_source"
FROM "nyc-open-data-uedp-fegm"
