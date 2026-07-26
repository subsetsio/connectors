-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "american_indianalaskan_native_ems_transports",
    "asian_ems_transports",
    "black_ems_transports",
    "hispanic_ems_transports",
    "multiracial_ems_transports",
    "white_ems_transports",
    "unknown_ems_transports",
    "total_ems_transports"
FROM "nyc-open-data-thjb-fm53"
