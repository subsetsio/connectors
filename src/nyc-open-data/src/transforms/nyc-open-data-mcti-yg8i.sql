-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "requestid",
    "_event" AS event,
    "agency",
    "_language" AS language,
    "_type" AS type,
    "numinterp",
    "date",
    "starttime",
    "endtime",
    "zip"
FROM "nyc-open-data-mcti-yg8i"
