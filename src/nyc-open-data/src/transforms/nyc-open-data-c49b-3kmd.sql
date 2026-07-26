-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "supervision_caseload_type",
    "_month" AS month,
    "_year" AS year,
    "supervision_caseload_count"
FROM "nyc-open-data-c49b-3kmd"
