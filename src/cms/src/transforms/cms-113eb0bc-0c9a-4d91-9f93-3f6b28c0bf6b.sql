-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEDICARE SPECIALTY CODE" AS medicare_specialty_code,
    "MEDICARE PROVIDER/SUPPLIER TYPE DESCRIPTION" AS medicare_provider_supplier_type_description,
    "PROVIDER TAXONOMY CODE" AS provider_taxonomy_code,
    "PROVIDER TAXONOMY DESCRIPTION:  TYPE, CLASSIFICATION, SPECIALIZATION" AS provider_taxonomy_description_type_classification_specialization
FROM "cms-113eb0bc-0c9a-4d91-9f93-3f6b28c0bf6b"
