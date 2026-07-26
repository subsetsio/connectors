-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fy",
    "agency",
    "organization",
    "project_title",
    "allocation"
FROM "nyc-open-data-y3ea-en4q"
