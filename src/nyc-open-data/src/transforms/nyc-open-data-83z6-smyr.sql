-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_2016_organization" AS 2016_organization,
    "project_address",
    "project_title",
    "council_district",
    "community_board",
    "_2016_award" AS 2016_award,
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-83z6-smyr"
