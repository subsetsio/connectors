-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are cumulative over the workbook coverage window, not annual observations; do not combine these metrics with the annual country rankings without accounting for the coverage years.
SELECT
    "coverage_start_year",
    "coverage_end_year",
    "rank",
    "country",
    "region",
    "documents",
    "citable_documents",
    "citations",
    "self_citations",
    "citations_per_document",
    "h_index"
FROM "scimago-journal-country-rank-country-rankings-history"
