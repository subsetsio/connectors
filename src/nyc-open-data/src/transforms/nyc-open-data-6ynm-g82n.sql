-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "dvstalkingarrests",
    "total_stalkingarrests",
    "dvstalkingarrestbx",
    "dvstalkingarrestbk",
    "dvstalkingarrestmn",
    "dvstalkingarrestqns",
    "dvstalkingarrestsi"
FROM "nyc-open-data-6ynm-g82n"
