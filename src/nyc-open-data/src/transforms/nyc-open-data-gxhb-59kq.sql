-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permitno",
    "permitexpiredate",
    "effectivedate",
    "permittype",
    "_location" AS location,
    "_valid" AS valid,
    "stateplate"
FROM "nyc-open-data-gxhb-59kq"
