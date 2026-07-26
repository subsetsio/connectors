-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "restaurantname",
    "seatingchoice",
    "legalbusinessname",
    "businessaddress",
    "restaurantinspectionid",
    "issidewaycompliant",
    "isroadwaycompliant",
    "skippedreason",
    "inspectedon",
    "agencycode",
    "postcode",
    "latitude",
    "longitude",
    "communityboard",
    "councildistrict",
    "censustract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-4dx7-axux"
