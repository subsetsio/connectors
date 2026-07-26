-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "featurestatus",
    "gispropnum",
    "_name" AS name,
    "nys_assembly",
    "nys_senate",
    "starea",
    "stlength",
    "_system" AS system,
    "us_congress",
    "multipolygon"
FROM "nyc-open-data-uwmn-v7un"
