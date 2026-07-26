-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "address",
    "landmark",
    "city",
    "state",
    "postcode",
    "_comments" AS comments,
    "latitude",
    "longitude",
    "borough",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract",
    "nta",
    "data_as_of_date"
FROM "nyc-open-data-pe54-wf39"
