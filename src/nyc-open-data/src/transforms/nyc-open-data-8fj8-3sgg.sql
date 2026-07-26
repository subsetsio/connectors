-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ceqr",
    "project_name",
    "milestone_name",
    "milestone_date"
FROM "nyc-open-data-8fj8-3sgg"
