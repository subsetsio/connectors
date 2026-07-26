-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "borocode",
    "boroname",
    "borocd",
    "coundist",
    "assemdist",
    "stsendist",
    "congdist",
    "_program" AS program,
    "site_id",
    "group_id",
    "borough",
    "ifoaddress",
    "onstreet",
    "fromstreet",
    "tostreet",
    "side_of_st",
    "racktype",
    "date_inst",
    "latitude",
    "longitude",
    "ntaname",
    "femafldz",
    "femafldt",
    "hrcevac"
FROM "nyc-open-data-592z-n7dk"
