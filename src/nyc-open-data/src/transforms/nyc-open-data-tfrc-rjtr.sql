-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "project_id",
    "title",
    "borough",
    "level_of_review",
    "agency",
    "certificate_number",
    "public_private",
    "_action" AS action,
    "project_type"
FROM "nyc-open-data-tfrc-rjtr"
