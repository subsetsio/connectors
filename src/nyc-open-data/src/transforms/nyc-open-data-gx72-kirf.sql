-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reinspectionid",
    "requestreinspection",
    "requestreinspectiondate",
    "reinspectsqft",
    "actualreinspectdate",
    "responsedate",
    "damageid",
    "damagetypecode"
FROM "nyc-open-data-gx72-kirf"
