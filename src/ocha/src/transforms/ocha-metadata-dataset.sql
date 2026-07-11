-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Dataset HDX ids are useful lookup values, but this model keeps the table keyless because the model verifier did not scan-verify dataset_hdx_id as row grain.
SELECT
    "dataset_hdx_id",
    "dataset_hdx_stub",
    "dataset_hdx_title",
    "hdx_provider_stub",
    "hdx_provider_name",
    "hdx_link",
    "hdx_api_link",
    "provider_hdx_link",
    "provider_hdx_api_link"
FROM "ocha-metadata-dataset"
