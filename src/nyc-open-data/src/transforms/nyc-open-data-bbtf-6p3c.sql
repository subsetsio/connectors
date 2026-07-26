-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acres",
    "address",
    "borough",
    "communityboard",
    "councildistrict",
    "dsfbldgcode",
    "gispropnum",
    "jurisdiction",
    "_location" AS location,
    "nys_assembly",
    "nys_senate",
    "us_congress",
    "zipcode",
    "multipolygon"
FROM "nyc-open-data-bbtf-6p3c"
