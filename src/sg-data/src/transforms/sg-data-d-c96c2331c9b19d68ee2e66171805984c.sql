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
FROM "sg-data-d-c96c2331c9b19d68ee2e66171805984c"
