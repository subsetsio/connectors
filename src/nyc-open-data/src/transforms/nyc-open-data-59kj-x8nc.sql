-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "litigationid",
    "buildingid",
    "boro",
    "housenumber",
    "streetname",
    "zip",
    "block",
    "lot",
    "casetype",
    "caseopendate",
    "casestatus",
    "openjudgement",
    "findingofharassment",
    "findingdate",
    "penalty",
    "respondent",
    "latitude",
    "longitude",
    "community_district",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-59kj-x8nc"
