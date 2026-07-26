-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid_1",
    "siteaddres",
    "_name" AS name,
    "boro",
    "shortname",
    "carshareor",
    "_type" AS type,
    "site_id",
    "cs_spaces_" AS cs_spaces,
    "status",
    "_offset" AS offset
FROM "nyc-open-data-j4y5-w7iq"
