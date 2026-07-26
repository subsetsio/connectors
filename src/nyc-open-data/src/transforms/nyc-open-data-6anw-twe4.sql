-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "developmentteamdwid",
    "projectid",
    "_type" AS type,
    "entityname",
    "firstname",
    "lastname",
    "entityindividualindicator",
    "parententityname",
    "individualrole",
    "individualtitle",
    "individualofficerequivalence",
    "careof",
    "number",
    "street",
    "apartmentsuitefloor",
    "city",
    "state",
    "postcode",
    "tradetype",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-6anw-twe4"
