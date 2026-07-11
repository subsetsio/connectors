-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Country names include territories and other SCImago reporting areas; use the `region` column when separating regional groups from country-level comparisons.
SELECT
    "year",
    "rank",
    "country",
    "region",
    "documents",
    "citable_documents",
    "citations",
    "self_citations",
    "citations_per_document",
    "h_index"
FROM "scimago-journal-country-rank-country-rankings"
