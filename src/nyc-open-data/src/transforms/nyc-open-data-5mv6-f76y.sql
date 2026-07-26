-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "boro",
    "legacy_id",
    "community",
    "the_geom",
    "council_di",
    "latitude",
    "longitude",
    "installati",
    "ppt_id",
    "street_add",
    "cross_1",
    "cross_2",
    "ixn_corner",
    "zip_code",
    "site_id",
    "activation",
    "install_co",
    "neighborho",
    "building_i",
    "borough_bl",
    "census_tra",
    "gf_permit",
    "x2",
    "y2"
FROM "nyc-open-data-5mv6-f76y"
