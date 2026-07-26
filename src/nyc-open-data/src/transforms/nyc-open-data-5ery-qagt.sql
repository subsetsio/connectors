-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "schoolname",
    "number",
    "street",
    "city",
    "state",
    "borough",
    "zipcode",
    "lastinspection",
    "permittee",
    "inspectiondate",
    "ptet",
    "site_type",
    "_level" AS level,
    "code",
    "violationdescription",
    "latitude",
    "longitude",
    "communityboard",
    "councildistrict",
    "censustract",
    "bin",
    "bbl",
    "nta",
    "borocode"
FROM "nyc-open-data-5ery-qagt"
