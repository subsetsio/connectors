-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "propnum",
    "prop_id",
    "boro",
    "ampsdistrict",
    "prop_name",
    "site_name",
    "prop_location",
    "site_location",
    "acres",
    "category",
    "subcategory",
    "rated",
    "reason_not_rated",
    "council_district",
    "zipcode",
    "communityboard",
    "jurisdiction",
    "nysassembly",
    "nyssenate",
    "uscongress",
    "precinct",
    "publicrestroom",
    "sourcefc"
FROM "nyc-open-data-xs5m-jrpm"
