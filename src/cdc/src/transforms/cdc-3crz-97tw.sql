-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Title" AS title,
    "Author(s)" AS author_s,
    "Journal" AS journal,
    CAST("Fiscal Year" AS BIGINT) AS fiscal_year,
    CAST("Publication Year" AS BIGINT) AS publication_year,
    "DOI Link" AS doi_link,
    "All Authors" AS all_authors,
    "Category Topics" AS category_topics,
    "Journal Information" AS journal_information,
    "Keyword Search Expanded" AS keyword_search_expanded,
    "URL" AS url,
    CAST("Row" AS BIGINT) AS row
FROM "cdc-3crz-97tw"
