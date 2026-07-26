-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "community_board",
    "first_name",
    "last_name",
    "zip_code_of_application",
    "recommending_official",
    "term_expires"
FROM "nyc-open-data-wbau-xy7g"
