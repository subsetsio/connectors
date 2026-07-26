-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kioskid",
    "_system" AS system,
    "borough",
    "parkdistrict",
    "gispropnum",
    "omppropid",
    "propertyname",
    "subpropertyname",
    "_location" AS location,
    "model",
    "submodel",
    "containersize",
    "status",
    "installationdate",
    "remove_date",
    "removal_reason",
    "status_change_date",
    "point"
FROM "nyc-open-data-r465-fr2q"
