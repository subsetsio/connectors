-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "business_name_dba",
    "address1",
    "address2",
    "city",
    "state",
    "zip",
    "community_board",
    "naics_code",
    "number_of_workerowners",
    "number_of_nonmember_workerowners",
    "subtype",
    "borough",
    "latitude",
    "longitude",
    "city_council",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-uxsz-6j5j"
