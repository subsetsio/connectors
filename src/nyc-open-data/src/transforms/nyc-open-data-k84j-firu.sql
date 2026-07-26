-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_2017_organization" AS 2017_organization,
    "project_address",
    "project_title",
    "council_district",
    "community_board",
    "_2017_award" AS 2017_award,
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-k84j-firu"
