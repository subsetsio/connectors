-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "stipulationid",
    "boroughname",
    "onstreetname",
    "fromstreetname",
    "tostreetname",
    "specificlocationname",
    "onboroughcode",
    "fromboroughcode",
    "communitydistrictleft",
    "communitydistrictright",
    "inspectiondistrict",
    "maintenancesector",
    "stipulationfulltext",
    "createdon",
    "modifiedon"
FROM "nyc-open-data-ge3f-inui"
