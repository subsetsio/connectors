-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are already aggregated for each Wikimedia project and month; sum across projects only when a cross-project total is intended.
SELECT
    "project",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "devices",
    "offset",
    "underestimate"
FROM "wikipedia-unique-devices"
