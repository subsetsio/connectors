-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "branch",
    "address",
    "phone",
    "latitude",
    "longitude",
    "hours_can_be_viewed_via_branch_url",
    "city",
    "postcode",
    "borough",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "point"
FROM "nyc-open-data-kh3d-xhq7"
