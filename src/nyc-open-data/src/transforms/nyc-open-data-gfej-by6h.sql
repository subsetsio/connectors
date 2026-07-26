-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "health_center",
    "street_address",
    "zip_code",
    "latitude",
    "longitude",
    "days_of_operation",
    "hours_of_operation",
    "telephone_number",
    "accept_walkins",
    "languages_other_than_english",
    "website",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "_location" AS location
FROM "nyc-open-data-gfej-by6h"
