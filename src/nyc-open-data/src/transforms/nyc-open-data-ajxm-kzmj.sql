-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "propid",
    "boro",
    "community_board",
    "council_district",
    "garden_name",
    "address",
    "size",
    "jurisdiction",
    "neighborhoodname",
    "cross_streets",
    "latitude",
    "longitude",
    "postcode",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-ajxm-kzmj"
