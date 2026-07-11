-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Resource HDX ids are useful lookup values, but this model keeps the table keyless because the model verifier did not scan-verify resource_hdx_id as row grain.
SELECT
    "resource_hdx_id",
    "dataset_hdx_id",
    "name",
    "format",
    "update_date",
    "is_hxl",
    "download_url",
    CAST("hapi_updated_date" AS TIMESTAMP) AS hapi_updated_date,
    "dataset_hdx_stub",
    "dataset_hdx_title",
    "dataset_hdx_provider_stub",
    "dataset_hdx_provider_name",
    "hdx_link",
    "hdx_api_link",
    "dataset_hdx_link",
    "dataset_hdx_api_link",
    "provider_hdx_link",
    "provider_hdx_api_link"
FROM "ocha-metadata-resource"
