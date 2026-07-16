-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "statistic_name",
    "statistic_description",
    "_lon" AS lon,
    "_lat" AS lat
FROM "usgs-statistic-codes"
