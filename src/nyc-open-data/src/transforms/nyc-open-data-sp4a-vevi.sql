-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "sfcode",
    "bldgcode",
    "schoolname",
    "siteaddress",
    "city",
    "zip",
    "accessibility",
    "longitude",
    "latitude",
    "koshermealtype"
FROM "nyc-open-data-sp4a-vevi"
