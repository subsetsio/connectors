-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_no",
    "agencies",
    "audit_title",
    "library_no",
    "issue_date",
    "website_link"
FROM "nyc-open-data-nekg-b6tw"
