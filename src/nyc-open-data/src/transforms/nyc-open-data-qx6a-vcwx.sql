-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "demographic_type",
    "demographic_category",
    "unsheltered",
    "unsheltered_1",
    "unstable",
    "unstable_1",
    "_stable" AS stable,
    "_stable_1" AS stable_1
FROM "nyc-open-data-qx6a-vcwx"
