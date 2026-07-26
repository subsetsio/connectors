-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "omoid",
    "omonumber",
    "buildingid",
    "boro_id",
    "boro",
    "housenumber",
    "streetname",
    "apartment",
    "zip",
    "block",
    "lot",
    "lifecycle",
    "worktypegeneral",
    "omostatusreason",
    "omoawardamount",
    "omocreatedate",
    "netchangeorders",
    "omoawarddate",
    "isaep",
    "iscommercialdemolition",
    "servicechargeflag",
    "femaeventid",
    "femaevent",
    "omodescription",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-mdbu-nrqn"
