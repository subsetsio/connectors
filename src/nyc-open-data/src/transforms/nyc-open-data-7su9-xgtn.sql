-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_of_program",
    "description",
    "_days" AS days,
    "times",
    "_location" AS location,
    "postcode",
    "borough",
    "phone_number",
    "email",
    "latitude",
    "longitude",
    "community_board",
    "community_council",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-7su9-xgtn"
