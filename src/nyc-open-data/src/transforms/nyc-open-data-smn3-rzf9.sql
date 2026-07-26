-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "_name" AS name,
    "_domain" AS domain,
    "latitude",
    "longitude",
    "interval",
    "timezone",
    "sens",
    "counter"
FROM "nyc-open-data-smn3-rzf9"
