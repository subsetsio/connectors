-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "schoolname",
    "number",
    "street",
    "address",
    "city",
    "borough",
    "zipcode",
    "last_inspection_date",
    "permittee",
    "inspection_date",
    "_level" AS level,
    "code",
    "description",
    "latitude",
    "longitude",
    "communityboard",
    "councildistrict",
    "censustract",
    "bin",
    "bbl",
    "nta",
    "borocode"
FROM "nyc-open-data-9hxz-c2kj"
