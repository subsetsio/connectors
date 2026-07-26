-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "total_investigations_assigned",
    "_month" AS month,
    "_year" AS year,
    "investigations_assigned_count"
FROM "nyc-open-data-vk9f-gvzq"
