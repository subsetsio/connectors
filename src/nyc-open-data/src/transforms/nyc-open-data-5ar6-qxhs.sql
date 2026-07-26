-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "borocode",
    "borocd",
    "assemdist",
    "stsendist",
    "congdist",
    "_location" AS location,
    "address",
    "borough",
    "postcode",
    "on_street",
    "to_street",
    "from_street",
    "_type" AS type,
    "partner",
    "status",
    "xcoordin",
    "ycoordin",
    "femafldz",
    "femafldt",
    "hrcevac",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract_2020",
    "bin",
    "bbl",
    "nta_2020"
FROM "nyc-open-data-5ar6-qxhs"
