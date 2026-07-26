-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "projectid",
    "buildingid",
    "reportingconstructiontype",
    "borough_code",
    "borough",
    "block",
    "lot",
    "bin",
    "housenumber",
    "streetname",
    "countedrentalunits",
    "countedhomeownershipunits",
    "allcountedunits",
    "totalbuildingunits",
    "basesquarefootage",
    "stories",
    "bbl",
    "community_board",
    "council_district",
    "census_tract",
    "nta",
    "latitude",
    "longitude",
    "postcode"
FROM "nyc-open-data-hu6m-9cfi"
