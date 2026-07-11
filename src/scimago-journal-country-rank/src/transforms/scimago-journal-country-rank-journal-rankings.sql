-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Journal rankings are annual source-title observations; `categories` and `areas` can contain multiple classifications in a single row.
SELECT
    "year",
    "rank",
    "sourceid",
    "title",
    "type",
    "issn",
    "publisher",
    "open_access",
    "open_access_diamond",
    "sjr",
    "sjr_best_quartile",
    "h_index",
    "total_docs_year",
    "total_docs_3years",
    "total_refs",
    "total_citations_3years",
    "citable_docs_3years",
    "citations_doc_2years",
    "ref_doc",
    "percent_female",
    "overton",
    "country",
    "region",
    "coverage",
    "categories",
    "areas"
FROM "scimago-journal-country-rank-journal-rankings"
