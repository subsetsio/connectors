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
    "category",
    "nearest_add",
    "on_street",
    "from_street",
    "to_street",
    "side_of_st",
    "installation_date",
    "asset_id",
    "asset_subtype",
    "latitude",
    "longitude",
    "siteid",
    "ntaname",
    "femafldz",
    "femafldt",
    "hrcevac"
FROM "nyc-open-data-esmy-s8q5"
