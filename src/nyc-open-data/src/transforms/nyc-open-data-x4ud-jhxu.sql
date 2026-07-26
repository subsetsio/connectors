-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fy",
    "agency",
    "organization_name",
    "project_title",
    "amount_requested",
    "funded_amount",
    "community_board",
    "organization_address",
    "city",
    "state",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-x4ud-jhxu"
