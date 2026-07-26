-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "licensee_number",
    "licensee_name",
    "alternate_name_of_licensee",
    "building",
    "street_address",
    "secondary_address",
    "city",
    "state",
    "post_code",
    "borough",
    "telephone_number",
    "last_updated_date",
    "last_updated_time",
    "latitude",
    "longitude",
    "community_board",
    "community_council",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-2n4x-d97d"
