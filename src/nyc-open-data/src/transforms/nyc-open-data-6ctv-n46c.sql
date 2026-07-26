-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "matter_id",
    "status",
    "file_number",
    "local_law_number",
    "primary_sponsor",
    "committee",
    "_name" AS name,
    "intro_date",
    "agenda_date",
    "passed_date",
    "enacted_date",
    "previous_file_number",
    "modified_date",
    "title",
    "summary"
FROM "nyc-open-data-6ctv-n46c"
