-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "doc_no",
    "document_title",
    "date",
    "link"
FROM "nyc-open-data-yv6j-r66f"
