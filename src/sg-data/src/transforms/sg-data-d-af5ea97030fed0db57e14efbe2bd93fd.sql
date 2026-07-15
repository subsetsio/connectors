-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
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
FROM "sg-data-d-af5ea97030fed0db57e14efbe2bd93fd"
