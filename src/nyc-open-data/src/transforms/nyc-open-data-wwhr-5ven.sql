-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vote_year",
    "council_district",
    "category",
    "project_number",
    "title",
    "description",
    "address",
    "votes",
    "winner",
    "_cost" AS cost,
    "bp_funding",
    "borough_code",
    "latitude",
    "longitude",
    "postcode",
    "community_board",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-wwhr-5ven"
