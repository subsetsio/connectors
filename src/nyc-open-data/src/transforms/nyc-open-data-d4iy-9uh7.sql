-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "development_name",
    "address",
    "status",
    "sponsor",
    "postcode",
    "_type" AS type,
    "latitude",
    "longitude",
    "community_board",
    "community_council",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-d4iy-9uh7"
