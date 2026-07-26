-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_system" AS system,
    "gispropnum",
    "omppropid",
    "publicname",
    "publiclocation",
    "parkdistrict",
    "borough",
    "shape"
FROM "nyc-open-data-j55h-3upk"
