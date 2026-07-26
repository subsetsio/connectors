-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_2015_organization" AS 2015_organization,
    "project_address",
    "project_title",
    "council_district",
    "community_board",
    "_2015_award" AS 2015_award,
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-6wee-b7wf"
