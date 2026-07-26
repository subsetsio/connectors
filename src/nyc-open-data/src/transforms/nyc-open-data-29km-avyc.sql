-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_id",
    "organization_id",
    "_name" AS name,
    "latitude",
    "longitude",
    "bbl",
    "bin",
    "cd",
    "council",
    "nta",
    "tract"
FROM "nyc-open-data-29km-avyc"
