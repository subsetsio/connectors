-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "schoolname",
    "number",
    "street",
    "suiteapt",
    "city",
    "state",
    "postcode",
    "latitude",
    "longitude",
    "contact",
    "telephone",
    "email",
    "web",
    "languagesoffered",
    "courseprice",
    "examprice",
    "date",
    "time",
    "borough",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "location_1"
FROM "nyc-open-data-auuc-fqzi"
