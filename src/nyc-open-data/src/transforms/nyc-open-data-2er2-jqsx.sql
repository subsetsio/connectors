-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "entity_name",
    "address",
    "floor",
    "borough",
    "state",
    "zip",
    "aed_numpersontrained",
    "aed_numaeds",
    "latitude",
    "longitude",
    "community_district",
    "council_district",
    "census_tract_2010",
    "nta_code",
    "bbl",
    "bin",
    "location_point",
    "location_type",
    "last_updated"
FROM "nyc-open-data-2er2-jqsx"
