-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hwoid",
    "hwonumber",
    "buildingid",
    "boroid",
    "boro",
    "housenumber",
    "streetname",
    "zip",
    "block",
    "lot",
    "lifecycle",
    "worktypegeneral",
    "hwostatusreason",
    "hwocreatedate",
    "isaep",
    "iscommercialdemolition",
    "femaeventid",
    "femaevent",
    "hwodescription",
    "hwoapprovedamount",
    "salestax",
    "adminfee",
    "chargeamount",
    "datetransferdof",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-sbnd-xujn"
