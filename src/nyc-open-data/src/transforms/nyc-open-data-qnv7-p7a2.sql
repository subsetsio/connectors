-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_system" AS system,
    "fountaintype",
    "position",
    "painted",
    "gispropnum",
    "propname",
    "omppropid",
    "borough",
    "fountaincount",
    "department",
    "district",
    "featurestatus",
    "point"
FROM "nyc-open-data-qnv7-p7a2"
