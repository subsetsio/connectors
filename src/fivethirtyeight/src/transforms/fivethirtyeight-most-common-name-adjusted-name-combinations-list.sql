-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "C0" AS c0,
    "FirstName" AS firstname,
    "Surname" AS surname,
    "Adjustment" AS adjustment,
    "cleanName" AS cleanname,
    "Estimate" AS estimate,
    "finalEstimate" AS finalestimate
FROM "fivethirtyeight-most-common-name-adjusted-name-combinations-list"
