-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "block",
    "lot",
    "address",
    "zip_code",
    "final_1819_actual_av",
    "tax_class",
    "bldg_class",
    "rpie_year",
    "status",
    "x_coordinate",
    "y_coordinate",
    "latitude",
    "longitude",
    "community_district",
    "city_council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-wvts-6tdf"
