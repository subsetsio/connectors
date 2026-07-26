-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_session" AS session,
    "borough",
    "swimming_pool",
    "class_type",
    "starttime",
    "total_registration",
    "total_attendance",
    "classname"
FROM "nyc-open-data-bzby-7sfr"
