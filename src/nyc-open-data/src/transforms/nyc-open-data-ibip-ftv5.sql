-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "conditionhazard",
    "_class" AS class,
    "number",
    "_type" AS type,
    "extent",
    "problem",
    "locationcomments",
    "priority",
    "cause",
    "feature"
FROM "nyc-open-data-ibip-ftv5"
