-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "newspaper_title",
    "issue_id",
    "issue_date",
    "edition",
    "page_id",
    "page_number",
    "article_id",
    "article_title",
    "article_text_1st50words",
    "contributor"
FROM "sg-data-d-4c3c3d7e5b29722187d69fe226a0acb7"
