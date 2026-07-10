-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "document_number",
    "type",
    "subtype",
    "title",
    "abstract",
    strptime("publication_date", '%Y-%m-%d')::DATE AS publication_date,
    strptime("signing_date", '%Y-%m-%d')::DATE AS signing_date,
    "citation",
    "start_page",
    "end_page",
    "page_length",
    "president_name",
    "president_id",
    "primary_agency_id",
    "primary_agency_name",
    "agency_ids",
    "agency_names",
    "html_url",
    "pdf_url"
FROM "federal-register-documents"
