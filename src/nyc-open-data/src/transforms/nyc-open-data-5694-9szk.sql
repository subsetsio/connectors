-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "name_of_business",
    "short_description",
    "address",
    "city",
    "state",
    "postcode",
    "phone_number",
    "which_type_of_business_is_this",
    "business_website_or_other_url",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-5694-9szk"
