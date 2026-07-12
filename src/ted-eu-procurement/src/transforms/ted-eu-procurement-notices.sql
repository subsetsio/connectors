-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current daily OJ S package extract, so it represents notices from one publication issue rather than a full historical backfill.
SELECT
    "asset_id",
    "package_issue_number",
    CAST("package_issue_token" AS BIGINT) AS package_issue_token,
    "package_publication_date",
    "xml_filename",
    "publication_number",
    "doc_id",
    "ojs_reference",
    "edition",
    CAST("schema_version" AS DOUBLE) AS schema_version,
    "xml_schema",
    "publication_date",
    "dispatch_date",
    "submission_deadline",
    "country",
    "document_type",
    "contract_nature",
    "procedure_type",
    "regulation",
    "authority_type",
    "main_activity",
    "title",
    "buyer_names",
    "cpv",
    "nuts",
    CAST("value" AS DOUBLE) AS value,
    "currency"
FROM "ted-eu-procurement-notices"
