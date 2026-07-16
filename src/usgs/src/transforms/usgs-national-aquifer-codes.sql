-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "national_aquifer_name",
    "_lon" AS lon,
    "_lat" AS lat
FROM "usgs-national-aquifer-codes"
