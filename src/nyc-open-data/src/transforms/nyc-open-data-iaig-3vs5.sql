-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fid",
    "objectid",
    "borocode",
    "borough",
    "brorocd",
    "council_district",
    "assemdist",
    "stsendist",
    "congdist",
    "site_id",
    "category",
    "address",
    "geocode_ad",
    "on_street",
    "cross_stre",
    "zipcode",
    "bar_quantity",
    "comdist",
    "installati",
    "routeid",
    "femafldz",
    "femafldt",
    "hrcevac",
    "latitude",
    "longitude",
    "community_board",
    "council_district_1",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-iaig-3vs5"
