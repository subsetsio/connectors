-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_received",
    "borough",
    "block",
    "lot",
    "_class" AS class,
    "community_board",
    "violation",
    "osm",
    "ccu",
    "sim",
    "bc",
    "other_log",
    "issue",
    "address",
    "cross_streets",
    "referredrouted_to",
    "resoultion",
    "date_closed",
    "results_of_inspection",
    "postcode",
    "latitude",
    "longitude",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-bheb-sjfi"
