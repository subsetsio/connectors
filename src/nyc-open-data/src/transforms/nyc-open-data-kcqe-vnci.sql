-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gispropnum",
    "sign_name",
    "recreation_category",
    "open_space_acres",
    "active_percent",
    "passive_percent",
    "active_acres",
    "passive_acres",
    "type_category",
    "_location" AS location,
    "zipcodes",
    "boro_census_tracts",
    "borough",
    "shape"
FROM "nyc-open-data-kcqe-vnci"
