-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Operation_number" AS operation_number,
    "Document_title" AS document_title,
    "IATI_Document_code" AS iati_document_code,
    "IATI_Document_code_name" AS iati_document_code_name,
    "Language" AS language,
    "Document_link" AS document_link,
    "Document_Type" AS document_type,
    "source_resource"
FROM "idb-idb-international-aid-transparency-initiative-iati-datasets-20042018"
