-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization",
    "project_title",
    "project_address",
    "community_board",
    "council_district",
    "fy18_award",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-66yh-nemi"
