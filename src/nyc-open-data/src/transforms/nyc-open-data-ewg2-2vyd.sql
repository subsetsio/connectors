-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "american_indianalaskan_native_removals",
    "american_indianalaskan_native_principal",
    "american_indianalaskan_native_superintendent",
    "american_indianalaskan_native_expulsions",
    "asian_removals",
    "asian_principal",
    "asian_superintendent",
    "asian_expulsions",
    "black_removals",
    "black_principal",
    "black_superintendent",
    "black_expulsions",
    "hispanic_removals",
    "hispanic_principal",
    "hispanic_superintendent",
    "hispanic_expulsions",
    "white_removals",
    "white_principal",
    "white_superintendent",
    "white_expulsions",
    "multiracial_removals",
    "multiracial_principal",
    "multiracial_superintendent",
    "multiracial_expulsions",
    "unknown_removals",
    "unknown_principal",
    "unknown_superintendent",
    "unknown_expulsions"
FROM "nyc-open-data-ewg2-2vyd"
