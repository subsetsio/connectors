-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "f1",
    "borough",
    "ifo_business",
    "applicant",
    "_year" AS year,
    "_location" AS location,
    "from_" AS from,
    "_to" AS to,
    "site_visit",
    "structure",
    "structur_1",
    "structur_2",
    "establishment",
    "parking_regulation",
    "application",
    "community_board_cb",
    "_2019_installation" AS 2019_installation,
    "_2019_removal" AS 2019_removal,
    "latitude",
    "longitude",
    "postcode",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "localtion1"
FROM "nyc-open-data-d83i-6us7"
