-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dataset",
    "copyright",
    "description",
    CAST("lastUpdated" AS TIMESTAMP) AS lastupdated,
    "dateRequested" AS daterequested,
    "termsOfUse" AS termsofuse,
    "license",
    "contact"
FROM "global-fund-datasetinformation"
